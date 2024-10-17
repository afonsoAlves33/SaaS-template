from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import Optional
from requests.exceptions import JSONDecodeError
from project.services.asaas.customer_manager import Customer_Manager
from project.services.asaas.payment_generator import Payment_Generator

router_customer_management = APIRouter()
router_payment_management = APIRouter()

CUSTOMER_ENDPOINT = "/customer"
PAYMENT_ENDPOINT = "/payment"
@router_customer_management.post(CUSTOMER_ENDPOINT)
def create_customer_in_payment_interface(
        name: str,
        cpfOrCnpj: str,
        cust_mngr: Customer_Manager = Depends(Customer_Manager)
):
    response = cust_mngr.create_a_customer(name=name, cpfCnpj=cpfOrCnpj)
    if "errors" in response.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["errors"])
    return response

@router_customer_management.get(CUSTOMER_ENDPOINT)
def list_customers(cust_mngr: Customer_Manager = Depends(Customer_Manager)):
    response = cust_mngr.get_all_customers()
    if "errors" in response.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["errors"])
    return response #   testar se o raise vai funcionar junto ao return
                    #   return cust_mngr.get_all_customers()

@router_customer_management.get(CUSTOMER_ENDPOINT+"/{customer_id}")
def list_customer(
        customer_id : str,
        cust_mngr: Customer_Manager = Depends(Customer_Manager)
):
    print(customer_id)
    try:
        response = cust_mngr.get_customer(customer_id)
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Customer does not exist")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if "errors" in response.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["errors"])
    return response


@router_payment_management.post(PAYMENT_ENDPOINT)
def generate_payment(
    customer_id : str,
    value: float,
    dueDate: str,
    billingType:  Optional[str] = "PIX",
    paymnt_mngr: Payment_Generator = Depends(Payment_Generator)
):
    dueDate = dueDate.replace("/", "-")
    try:
        response = paymnt_mngr.generate_payment(customer_id=customer_id, value=value, dueDate=dueDate, billingType=billingType)
    except Exception as e:
        print(e)
    
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate payment with this data")
    if "errors" in response.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["errors"])
    return response

@router_payment_management.get(PAYMENT_ENDPOINT)
def generate_payment(
    paymnt_mngr: Payment_Generator = Depends(Payment_Generator)
):
    try:
        response = paymnt_mngr.list_all_payments()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not fetch this data")
    if "errors" in response.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["errors"])
    return response

