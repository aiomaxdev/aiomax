from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class Subscription(BaseModel):
    """Модель подписки на Webhook"""
    url: str
    time: int
    update_types: Optional[List[str]] = None


class SubscriptionsResponse(BaseModel):
    """Ответ от GET /subscriptions"""
    subscriptions: List[Subscription]


class CreateSubscriptionRequest(BaseModel):
    """Запрос на создание подписки"""
    url: str
    update_types: Optional[List[str]] = None
    secret: Optional[str] = None


class SubscriptionResponse(BaseModel):
    """Ответ от POST/DELETE /subscriptions"""
    success: bool
    message: Optional[str] = None