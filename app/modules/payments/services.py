import os
import requests
from datetime import datetime, timezone
from bson import ObjectId
from app.extensions import mongo
from app.core.base_service import BaseService
from .models import PaymentTransaction

# ── Variables de entorno ────────────────────────────────────────────────────
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL", "https://api-m.sandbox.paypal.com")

# ── Precios por plan (USD) ──────────────────────────────────────────────────
PLAN_PRICES = {
    "basic":        0.00,
    "professional": 9.99,
    "business":    29.99,
}

PLAN_DESCRIPTIONS = {
    "basic":        "Plan Básico – MindVoice",
    "professional": "Plan Profesional – MindVoice",
    "business":     "Plan Business – MindVoice",
}


class PayPalService:
    """Maneja todas las interacciones con la API REST de PayPal."""

    # ── Auth ────────────────────────────────────────────────────────────────
    @staticmethod
    def _get_access_token() -> str:
        """Obtiene un access-token OAuth 2.0 de PayPal."""
        if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
            raise ValueError(
                "Las variables de entorno PAYPAL_CLIENT_ID y PAYPAL_CLIENT_SECRET no están configuradas."
            )
        url = f"{PAYPAL_BASE_URL}/v1/oauth2/token"
        response = requests.post(
            url,
            auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()["access_token"]

    @classmethod
    def _headers(cls) -> dict:
        return {
            "Authorization": f"Bearer {cls._get_access_token()}",
            "Content-Type": "application/json",
        }

    # ── Crear orden ─────────────────────────────────────────────────────────
    @classmethod
    def create_order(cls, plan: str, return_url: str, cancel_url: str) -> dict:
        """Crea una orden de PayPal y devuelve el order_id y la URL de aprobación."""
        amount = PLAN_PRICES[plan]
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders"
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "description": PLAN_DESCRIPTIONS[plan],
                    "amount": {
                        "currency_code": "USD",
                        "value": f"{amount:.2f}",
                    },
                }
            ],
            "application_context": {
                "return_url": return_url,
                "cancel_url": cancel_url,
                "brand_name": "MindVoice",
                "user_action": "PAY_NOW",
            },
        }
        response = requests.post(url, json=payload, headers=cls._headers(), timeout=15)
        response.raise_for_status()
        data = response.json()

        approve_url = next(
            (link["href"] for link in data.get("links", []) if link["rel"] == "approve"),
            None,
        )
        return {
            "order_id": data["id"],
            "approve_url": approve_url,
            "plan": plan,
            "amount": amount,
            "currency": "USD",
        }

    # ── Capturar pago ───────────────────────────────────────────────────────
    @classmethod
    def capture_order(cls, order_id: str) -> dict:
        """Captura el pago de una orden aprobada."""
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture"
        response = requests.post(url, headers=cls._headers(), timeout=15)
        response.raise_for_status()
        return response.json()

    # ── Verificar estado de orden ───────────────────────────────────────────
    @classmethod
    def get_order(cls, order_id: str) -> dict:
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}"
        response = requests.get(url, headers=cls._headers(), timeout=15)
        response.raise_for_status()
        return response.json()


class PaymentService(BaseService):
    """Gestiona transacciones en la base de datos y actualiza el plan del usuario."""

    collection_name = "payment_transactions"

    # ── Registro de transacción ─────────────────────────────────────────────
    @classmethod
    def save_transaction(cls, user_id: str, order_id: str, plan: str,
                         amount: float, status: str = "pending", paypal_details: dict = None) -> str:
        tx = PaymentTransaction(
            user_id=user_id,
            order_id=order_id,
            plan=plan,
            amount=amount,
            status=status,
            paypal_details=paypal_details or {},
        )
        return str(cls.create(tx.to_dict()))

    @classmethod
    def update_transaction_status(cls, order_id: str, status: str, paypal_details: dict = None):
        collection = cls.get_collection()
        update_data = {
            "status": status,
            "updatedAt": datetime.now(timezone.utc),
        }
        if paypal_details:
            update_data["paypalDetails"] = paypal_details
        collection.update_one({"orderId": order_id}, {"$set": update_data})

    @classmethod
    def get_by_order_id(cls, order_id: str):
        return cls.get_collection().find_one({"orderId": order_id})

    @classmethod
    def get_by_user_id(cls, user_id: str):
        return list(cls.get_collection().find({"userId": user_id}))

    # ── Actualizar plan del usuario ─────────────────────────────────────────
    @classmethod
    def upgrade_user_plan(cls, user_id: str, plan: str):
        mongo.db["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"plan": plan, "updatedAt": datetime.now(timezone.utc)}},
        )
