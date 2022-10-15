#!/usr/bin/env python

import uvicorn

import config

if __name__ == "__main__":
    uvicorn.run(
        "SoapRecordSupport:app",
        host=config.http_host,
        port=config.http_port,
        reload=config.env != 'prd' # prdでない時=devの時はホットリロードを有効にする。
    )
