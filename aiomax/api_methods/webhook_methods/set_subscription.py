from aiomax.api_methods.base_method import BaseMethod
from aiomax.enums.request_metod import RequestMethod
from typing import Optional, List
from aiomax.models.webhook import SubscriptionResponse


class SetSubscription(BaseMethod):
    """Создание подписки на Webhook"""
    path = "subscriptions"
    method = RequestMethod.POST
    response_model = SubscriptionResponse

    def __init__(
        self,
        *,
        url: str,
        update_types: Optional[List[str]] = None,
        secret: Optional[str] = None
    ):
        json_data = {
            "url": url,
        }

        if update_types is not None:
            json_data["update_types"] = update_types

        if secret is not None:
            json_data["secret"] = secret

        super().__init__(json=json_data)