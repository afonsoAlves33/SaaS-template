from time import sleep
from fastapi import BackgroundTasks, Depends, FastAPI
from auth.routes import router

app = FastAPI()

@app.get("/")
def index():
    return {"It's working"}

async def m_number(n):
        sleep(5)
        print("Time Awaited - ", (int(n) * 1000))

@app.get("/get_m/")
async def get_query(background_tasks: BackgroundTasks, n):
    background_tasks.add_task(m_number, n)

    return "Number multriplying on background"
