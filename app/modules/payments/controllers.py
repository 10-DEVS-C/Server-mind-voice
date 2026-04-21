from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
import requests as http_requests

from app.core.auth_utils import get_current_user_id
from .schemas import (
    CreateOrderSchema,
    CaptureOrderSchema,
    CreateOrderResponseSchema,
    PaymentTransactionSchema,
    VALID_PLANS,
)
from .services import PayPalService, PaymentService, PLAN_PRICES

blp = Blueprint("payments", __name__, description="Gestión de pagos y planes de usuario")


@blp.route("/create-order")
class CreateOrderResource(MethodView):
    @jwt_required()
    @blp.arguments(CreateOrderSchema)
    @blp.response(201, CreateOrderResponseSchema)
    def post(self, data):
        """Crear una orden de PayPal para cambiar de plan

        Devuelve el `order_id` y la `approve_url` a la que debe redirigirse el usuario
        para aprobar el pago en PayPal. Una vez aprobado, usa el endpoint
        `/payments/capture-order` para confirmar y actualizar el plan.
        """
        plan = data["plan"]

        if PLAN_PRICES[plan] == 0.0:
            abort(400, message="El plan básico es gratuito. No requiere pago.")


        user_id = get_current_user_id()

        # URLs de retorno configurables vía cabecera o valores por defecto
        return_url = request.headers.get(
            "X-Return-Url",
            f"{request.host_url}payments/capture-order"
        )
        cancel_url = request.headers.get(
            "X-Cancel-Url",
            f"{request.host_url}payments/cancel"
        )

        try:
            order = PayPalService.create_order(plan, return_url, cancel_url)
        except ValueError as exc:
            abort(503, message=str(exc))
        except http_requests.HTTPError as exc:
            detail = exc.response.text if exc.response is not None else str(exc)
            abort(502, message=f"Error al comunicarse con PayPal: {detail}")
        except Exception as exc:
            print("Error inesperado al crear orden de PayPal:", exc)
            abort(500, message=str(exc))

        # Guardar transacción pendiente en BD
        PaymentService.save_transaction(
            user_id=str(user_id),
            order_id=order["order_id"],
            plan=plan,
            amount=order["amount"],
            status="pending",
        )

        return order


@blp.route("/capture-order")
class CaptureOrderResource(MethodView):
    @jwt_required()
    @blp.arguments(CaptureOrderSchema)
    @blp.response(200, PaymentTransactionSchema)
    def post(self, data):
        """Capturar el pago y actualizar el plan del usuario

        Debe llamarse después de que el usuario haya aprobado el pago en PayPal.
        Si el pago es exitoso, el plan del usuario se actualiza automáticamente.
        """
        order_id = data["order_id"]
        user_id = get_current_user_id()

        # Verificar que la transacción pertenece al usuario autenticado
        transaction = PaymentService.get_by_order_id(order_id)
        if not transaction:
            abort(404, message="Orden no encontrada.")
        if str(transaction["userId"]) != str(user_id):
            abort(403, message="No tienes permiso para capturar esta orden.")
        if transaction["status"] == "completed":
            abort(409, message="Esta orden ya fue procesada.")

        # Capturar pago en PayPal
        try:
            capture_result = PayPalService.capture_order(order_id)
        except ValueError as exc:
            abort(503, message=str(exc))
        except http_requests.HTTPError as exc:
            detail = exc.response.text if exc.response is not None else str(exc)
            PaymentService.update_transaction_status(order_id, "failed")
            abort(502, message=f"Error al capturar el pago en PayPal: {detail}")
        except Exception as exc:
            PaymentService.update_transaction_status(order_id, "failed")
            abort(500, message=str(exc))

        capture_status = capture_result.get("status", "")

        if capture_status != "COMPLETED":
            PaymentService.update_transaction_status(order_id, "failed", capture_result)
            abort(402, message=f"El pago no fue completado. Estado: {capture_status}")

        # Actualizar transacción y plan del usuario
        plan = transaction["plan"]
        PaymentService.update_transaction_status(order_id, "completed", capture_result)
        PaymentService.upgrade_user_plan(str(user_id), plan)

        updated_tx = PaymentService.get_by_order_id(order_id)
        # Serializar _id para la respuesta
        updated_tx["_id"] = str(updated_tx["_id"])
        return updated_tx


@blp.route("/my-transactions")
class MyTransactionsResource(MethodView):
    @blp.response(200, PaymentTransactionSchema(many=True))
    @jwt_required()
    def get(self):
        """Obtener el historial de transacciones del usuario autenticado"""
        user_id = get_current_user_id()
        transactions = PaymentService.get_by_user_id(str(user_id))
        for tx in transactions:
            tx["_id"] = str(tx["_id"])
        return transactions


@blp.route("/plans")
class PlansResource(MethodView):
    @blp.response(200)
    def get(self):
        """Obtener los planes disponibles y sus precios"""
        return {
            "plans": [
                {
                    "name": "basic",
                    "price": PLAN_PRICES["basic"],
                    "currency": "USD",
                    "description": "Hasta 5 elementos. Acceso básico.",
                },
                {
                    "name": "professional",
                    "price": PLAN_PRICES["professional"],
                    "currency": "USD",
                    "description": "Hasta 25 elementos. Funciones avanzadas.",
                },
                {
                    "name": "business",
                    "price": PLAN_PRICES["business"],
                    "currency": "USD",
                    "description": "Elementos ilimitados. Acceso completo.",
                },
            ]
        }
