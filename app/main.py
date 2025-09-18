from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from app.api.v1 import answer_router, auth_router, question_router
from app.errors import BaseError
from app.core import log_by_status
import time

app = FastAPI()


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):

    code = exc.status
    message_data = (
        f"HTTP:{request.method} "
        f"URL:{request.url} "
        f"HANDLED_ERROR:'{exc.text}' "
        f"STATUS:{code}"
    )

    log_by_status(code, message_data)

    return JSONResponse(
        status_code=code,
        content={"detail": exc.text},
    )


@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception):

    code = 500
    message_data = f"HTTP:{request.method} URL:{request.url} ERROR:{str(exc)}"

    log_by_status(code, message_data)

    return JSONResponse(
        status_code=code,
        content={"detail": f"Internal server error occured, see logs for more info."},
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time

    code = response.status_code
    message_data = (
        f"HTTP:{request.method} "
        f"URL:{request.url} "
        f"STATUS:{code} "
        f"TIME_MS:{round(process_time*1000, ndigits=3)}"
    )

    log_by_status(code, message_data)

    return response


app.include_router(auth_router)
app.include_router(question_router)
app.include_router(answer_router)
