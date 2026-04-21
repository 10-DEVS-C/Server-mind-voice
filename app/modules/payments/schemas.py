from marshmallow import Schema, fields, validate, pre_load

VALID_PLANS = ["basic", "professional", "business"]

class CreateOrderSchema(Schema):
    plan = fields.String(
        required=True,
        validate=validate.OneOf(VALID_PLANS),
        metadata={"description": "Plan a adquirir: basic, professional o business"}
    )

    @pre_load
    def normalize_plan(self, data, **kwargs):
        if isinstance(data.get("plan"), str):
            data["plan"] = data["plan"].lower()
        return data

class CaptureOrderSchema(Schema):
    order_id = fields.String(required=True, metadata={"description": "ID de la orden de PayPal"})

class PaymentTransactionSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(dump_only=True)
    orderId = fields.String(dump_only=True)
    plan = fields.String(dump_only=True)
    amount = fields.Float(dump_only=True)
    currency = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    paypalDetails = fields.Dict(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)

class CreateOrderResponseSchema(Schema):
    order_id = fields.String()
    approve_url = fields.String()
    plan = fields.String()
    amount = fields.Float()
    currency = fields.String()
