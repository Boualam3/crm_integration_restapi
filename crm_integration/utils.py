from hubspot import HubSpot
from django.conf import settings


def get_hubspot_client():
    """
    Initializes and return the hubspot client
    Raises:
        ValueError: if the hubspot tken is not provided (initially via .env file) then in settings.base
    """
    access_token = settings.HUBSPOT_ACCESS_TOKEN
    if not access_token:
        raise ValueError("Hubspot AccessToken is required!")

    return HubSpot(access_token=access_token)
