from fastapi import fastapi, APIRouter


router_controllers_customers = APIRouter(prefix='/customers')

@router_controllers_customers.post("/SLA")
def sla():
    return
