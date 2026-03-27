from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.request_metod import RequestMethod
from aiomax.models.webhook import SubscriptionResponse


class DeleteSubscription(BaseMethod):
    """Отписка от Webhook"""
    path = "subscriptions"
    method = RequestMethod.DELETE
    response_model = SubscriptionResponse

    def __init__(self, *, url: str):
        params = {"url": url}
        super().__init__(params=params)