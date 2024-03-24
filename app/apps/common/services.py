import logging
import os
import uuid

from target365_sdk import ApiClient
from target365_sdk.models.out_message import OutMessage

from apps.common.functions import to_norwegian_datetime


class SmsService:
    logger = logging.getLogger(__name__)

    company_name = os.getenv('COMPANY_NAME')
    company_full_address = os.getenv('COMPANY_FULL_ADDRESS')
    company_phone = os.getenv('COMPANY_PHONE')

    sender = 'Barbershop'
    base_url = os.getenv('SMS_CLIENT_URL')
    key_name = os.getenv('SMS_CLIENT_KEY_NAME')
    private_key = os.getenv('SMS_CLIENT_PRIVATE_KEY')
    target365_client = ApiClient(base_url, key_name, private_key)

    no_reply_email = os.getenv('DEVELOPER_NO_REPLY_EMAIL')

    @classmethod
    def send_otc(cls, recipient: str, otc: int):
        content = f"Din bekreftelseskode er: {str(otc)}"
        cls.send_sms(recipient=recipient, content=content)

    @classmethod
    def send_generated_password(cls, recipient: str, password: str):
        content = f"Ditt passord er: {password}"
        cls.send_sms(recipient=recipient, content=content)

    @classmethod
    def send_cancellation_code(cls, recipient: str, verification_code: int):
        content = f"Bekreft kanselering med denne koden: {str(verification_code)}"
        cls.send_sms(recipient=recipient, content=content)

    @classmethod
    def send_confirmation(cls, recipient: str, cancellation_link: str, start_time: str):
        content = (
            "Din reservasjon er bekreftet!\n\n"
            f"Tidspunkt: {to_norwegian_datetime(start_time)}\n"
            f"Sted: {cls.company_full_address}\n\n"
            f"Avbestill ved å klikke på denne linken: {cancellation_link}"
        )

        cls.send_sms(recipient=recipient, content=content)

    @classmethod
    def send_sms(cls, recipient, content):
        message = OutMessage()
        message.transactionId = str(uuid.uuid4())
        message.sender = cls.sender
        message.recipient = "+47" + recipient
        message.content = content

        try:
            cls.target365_client.create_out_message(message)
        except Exception as e:
            logging.error(f"Error initializing ApiClient: {str(e)}")
