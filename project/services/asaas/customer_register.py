import requests

URL_CUSTOMERS = "https://sandbox.asaas.com/api/v3/customers"
API_TOKEN = "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwOTA1Nzc6OiRhYWNoXzI4NjdkNDY3LTUxNDEtNGI5NC1hYzcyLWY5MGNjMWY3YjE4OQ=="

class Customer_Register():
    def __init__(self, Payment_Interface):
        self.payment_interface = Payment_Interface

    def create_a_customer(self, name: str, cpfCnpj: str, **kwargs) -> dict:
        """
        Cria um novo cliente na API do Asaas.

        :param name: mandatory
        :param cpfCnpj: client's CPF or CNPJ. It's mandatory
        :param kwargs: You can set: email, phone, mobilePhone, address, addressNumber, complement, province, postalCode, externalReference, notificationDisabled, additionalEmails, groupName, observations, company
        :return: dict
        """
        url = URL_CUSTOMERS
        data = {
            "name": name,
            "cpfCnpj": cpfCnpj
        }
        data.update(kwargs)
        response = requests.post(
            url=url,
            headers={
                "access_token": API_TOKEN
            },
            json=data
        )
        return response.json()
