import requests
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from project.services.asaas.config import Endpoints
from datetime import date
import os

load_dotenv()

test_route = APIRouter()

API_TOKEN = os.getenv("API_TOKEN")
URL_PAYMENT = Endpoints.ASAAS_PAYMENTS


class Payment_Generator():

    def generate_payment(self, customer_id: str, value: float, dueDate: date,  billingType: str, **kwargs) -> dict:
        url = URL_PAYMENT
        data = {
            "customer": customer_id,
            "billingType": billingType,
            "value": value,
            "dueDate": dueDate
        }
        data.update(kwargs)
        try:
            response = requests.post(
                url=url,
                headers={
                "access_token": API_TOKEN
                },
                data=data
            )
        except Exception as e:
            raise e
        print(response.json())
        return response.json()

    def list_all_payments(self, **kwargs) -> dict:
        url = URL_PAYMENT
        query_params = {}
        query_params.update(kwargs)
        try:
            response = requests.post(
                url=url,
                headers={
                    "access_token": API_TOKEN
                },
                params=query_params
            )
        except Exception as e:
            raise e
        print(response.json())
        return response.json()
