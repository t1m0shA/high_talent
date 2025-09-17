from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import answer_router, auth_router, question_router
from app.errors import BaseError

app = FastAPI()


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):

    return JSONResponse(
        status_code=exc.status,
        content={"detail": exc.text},
    )


@app.exception_handler(Exception)
async def unknown_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error occured, see logs for more info."},
    )


app.include_router(auth_router)
app.include_router(question_router)
app.include_router(answer_router)
