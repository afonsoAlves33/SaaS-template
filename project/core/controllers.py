from fastapi import APIRouter, Depends, HTTPException, status
from requests.exceptions import JSONDecodeError
from project.services.asaas.customer_manager import Customer_Manager

router_customer_management = APIRouter()
CUSTOMER_ENDPOINT = "/customer"
@router_customer_management.post(CUSTOMER_ENDPOINT)
def create_customer_in_payment_interface(
        name: str,
        cpfOrCnpj: str,
        cust_mngr: Customer_Manager = Depends(Customer_Manager)
):
    response = cust_mngr.create_a_customer(name=name, cpfCnpj=cpfOrCnpj)
    return response

@router_customer_management.get(CUSTOMER_ENDPOINT)
def list_customers(cust_mngr: Customer_Manager = Depends(Customer_Manager)):
    response = cust_mngr.get_all_customers()
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
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response


