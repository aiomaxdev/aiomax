# aiomax/models/attachments/request_payloads.py
from typing import List, Literal, Optional, Union, Annotated
from pydantic import BaseModel, Field

from aiomax.models.attachments.image import PhotoAttachmentRequestPayload
from aiomax.models.keyboard.callback_button import CallbackButton
from aiomax.models.keyboard.link_button import LinkButton
from aiomax.models.keyboard.message_button import MessageButton
from aiomax.models.keyboard.open_app_button import OpenAppButton
from aiomax.models.keyboard.request_contact_button import RequestContactButton
from aiomax.models.keyboard.request_geo_locatiom_button import RequestGeoLocationButton

# --- 1. Payload для клавиатуры (кнопки) ---
class InlineKeyboardAttachmentRequestPayload(BaseModel):
    """Payload для inline_keyboard при отправке"""
    buttons: List[List[Union[
        'CallbackButton',
        'LinkButton', 
        'RequestGeoLocationButton',
        'RequestContactButton',
        'OpenAppButton',
        'MessageButton'
    ]]]

class PhotoAttachmentRequestPayload(BaseModel):
    url: Optional[str]=None
    token: Optional[str]=None
    photos: Optional[str]=None
    
# --- 2. Payload для контакта ---
class ContactAttachmentRequestPayload(BaseModel):
    """Payload для контакта при отправке"""
    name: Optional[str] = None
    contact_id: Optional[int] = None
    vcf_info: Optional[str] = None
    vcf_phone: Optional[str] = None

# --- 3. Payload для геолокации ---
class LocationAttachmentRequestPayload(BaseModel):
    """Payload для локации при отправке"""
    latitude: float
    longitude: float

# --- 4. Универсальный payload для медиа (аудио/видео/файл) ---
class UploadedInfo(BaseModel):
    """Информация о загруженном файле"""
    token: Optional[str] = None

class MediaAttachmentRequestPayload(BaseModel):
    """Базовый класс для медиа"""
    url: Optional[str] = None
    token: Optional[str] = None

# --- 5. Стилизуем AttachmentRequest через Union ---
# Теперь он понимает разные типы вложений

class InlineKeyboardAttachmentRequest(BaseModel):
    type: Literal["inline_keyboard"]
    payload: InlineKeyboardAttachmentRequestPayload

class PhotoAttachmentRequest(BaseModel):
    type: Literal["image"]
    payload: 'PhotoAttachmentRequestPayload'  # из твоего кода

class ContactAttachmentRequest(BaseModel):
    type: Literal["contact"]
    payload: ContactAttachmentRequestPayload

class LocationAttachmentRequest(BaseModel):
    type: Literal["location"]
    payload: LocationAttachmentRequestPayload

class FileAttachmentRequest(BaseModel):
    type: Literal["file"]
    payload: UploadedInfo

class AudioAttachmentRequest(BaseModel):
    type: Literal["audio"]
    payload: UploadedInfo

class VideoAttachmentRequest(BaseModel):
    type: Literal["video"]
    payload: UploadedInfo

# === ГЛАВНОЕ: полиморфный тип для вложений ===
AttachmentRequest = Annotated[
    Union[
        InlineKeyboardAttachmentRequest,
        PhotoAttachmentRequest,
        ContactAttachmentRequest,
        LocationAttachmentRequest,
        FileAttachmentRequest,
        AudioAttachmentRequest,
        VideoAttachmentRequest,
    ],
    Field(discriminator="type")  # Pydantic сам выберет нужную модель по полю "type"
]