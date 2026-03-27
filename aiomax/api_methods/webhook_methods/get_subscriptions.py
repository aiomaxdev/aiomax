from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.request_metod import RequestMethod
from typing import Optional, List
from aiomax.models.webhook import SubscriptionsResponse


class GetSubscriptions(BaseMethod):
    """Получение списка подписок на Webhook"""
    path = "subscriptions"
    method = RequestMethod.GET
    response_model = SubscriptionsResponse

    def __init__(self):
        super().__init__(params={})