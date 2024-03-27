# utils.py

import requests
import uuid

import random

def generate_confirmation_code():
    confirmation_code = ''.join(random.choices('0123456789', k=4))
    return confirmation_code


def send_sms(phone_number, confirmation_code):
    login = 'nurmuhammed'
    password = 'oRXcgAEn'
    transaction_id = str(uuid.uuid4())
    sender = 'SMSPRO.KG'
    text = f'Your confirmation code id: {confirmation_code}'  # Здесь можно использовать ваш шаблон сообщения с кодом подтверждения

    xml_data = f"""
    <?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <message>
        <login>{login}</login>
        <pwd>{password}</pwd>
        <id>{transaction_id}</id>
        <sender>{sender}</sender>
        <text>{text}</text>
        <phones>
            <phone>{phone_number}</phone>
        </phones>
    </message>
    """

    url = 'https://smspro.nikita.kg/api/message'
    headers = {'Content-Type': 'application/xml'}

    response = requests.post(url, data=xml_data, headers=headers)
    if response.status_code == 200:
        print('SMS sent successfully')
    else:
        print('Failed to send SMS')

