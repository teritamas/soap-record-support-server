import logging

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

from fastapi import FastAPI

from SoapRecordSupport.router import router

app = FastAPI()

app.include_router(router)
