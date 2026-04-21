from datetime import datetime

class PaymentTransaction:
    def __init__(self, user_id, order_id, plan, amount, currency="USD", status="pending", paypal_details=None):
        self.userId = user_id
        self.orderId = order_id
        self.plan = plan
        self.amount = amount
        self.currency = currency
        self.status = status          # pending | completed | failed
        self.paypalDetails = paypal_details or {}
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.userId,
            "orderId": self.orderId,
            "plan": self.plan,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "paypalDetails": self.paypalDetails,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
