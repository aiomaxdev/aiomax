from enum import Enum


class ButtonType(str, Enum):
    CALLBACK="callback"
    LINK="link"
    REQUEST_GEO_LOCATION="request_geo_location"
    REQUEST_CONTACT="request_contact"
    OPEN_APP="open_app"
    MESSAGE="message"