# MIT License
#
# Copyright (c) 2024 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.core.logger import get_logger
from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException, status
from app.core.configs import configs

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if configs.tyran_api_key == "" or api_key == configs.tyran_api_key:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
    )


async def log_requests(request: Request, call_next):
    log = get_logger()
    log.info(f"Received {request.method} request to {request.url}")
    response = await call_next(request)
    log.info(f"Returning {response.status_code} response")
    return response


async def global_exception_handler(request: Request, exc: Exception):
    log.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def setup_middleware(app: FastAPI):
    app.middleware("http")(log_requests)
    app.exception_handler(Exception)(global_exception_handler)
