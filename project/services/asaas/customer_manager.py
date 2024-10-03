import requests
from fastapi import APIRouter, Request

URL_CUSTOMERS = "https://sandbox.asaas.com/api/v3/customers"
API_TOKEN = "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwOTA1Nzc6OiRhYWNoX2NhMGFjNjg3LTc2NjUtNDIzZi04NWQ4LWVhYmZmOWYxYjNkMw=="


router_tests = APIRouter()

class Customer_Manager():
    def __init__(self):
        pass

    def create_a_customer(self, name: str, cpfCnpj: str, **kwargs) -> dict:
        """
        :param name: string - mandatory - Name of the customer
        :param cpfCnpj: string - mandatory - CPF or CNPJ of the customer
        :param email: string - Email of the customer
        :param phone: string - Landline phone number
        :param mobilePhone: string - Mobile phone number
        :param address: string - Street address
        :param addressNumber: string - Address number
        :param complement: string - Address complement
        :param province: string - Neighborhood
        :param postalCode: string - Postal code of the address
        :param externalReference: string - Identifier of the customer in your system
        :param notificationDisabled: boolean - true to disable sending billing notifications
        :param additionalEmails: string - Additional emails for sending billing notifications, separated by ","
        :param municipalInscription: string - Municipal registration of the customer
        :param stateInscription: string - State registration of the customer
        :param observations: string - Additional observations
        :param groupName: string - Name of the group to which the customer belongs
        :param company: string - Company
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

    def get_customers(**kwargs) -> dict:
        """
        :param offset: integer - Starting element of the list
        :param limit: integer - ≤ 100 - Number of elements in the list (max: 100)
        :param name: string - Filter by customer's name
        :param email: string - Filter by customer's email
        :param cpfCnpj: string - Filter by CPF or CNPJ
        :param groupName: string - Filter by group
        :param externalReference: string - Filter by the identifier from your system
        :return: dict
        """
        url = URL_CUSTOMERS
        query_params = {}
        query_params.update(kwargs)
        response = requests.get(
            url=url,
            headers={
                "access_token": API_TOKEN
            },
            params=query_params
        )
        return response.json()

