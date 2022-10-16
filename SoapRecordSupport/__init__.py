import logging

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from SoapRecordSupport.router import router

description = f"""
看護師の看護記録の記入の支援を行うレコサポAPIのAPI仕様書です。
"""

app = FastAPI(
    title="レコサポAPI",
    description=description,
    version="0.0.1",
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
