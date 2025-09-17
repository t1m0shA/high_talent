from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.questions_routes import router as question_router
from app.api.v1.answers_routes import router as answer_router
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
