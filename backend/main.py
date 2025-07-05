import os
from dotenv import load_dotenv

from fastapi import FastAPI, Response, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn


load_dotenv()

HOST = os.getenv("RUN_HOST")
PORT = int(os.getenv("RUN_PORT"))


app = FastAPI()

# Custom handler for 422 errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "message": "Invalid request payload"
        },
    )

# Custom handler for 405 errors
@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=405,
        content={
            "status": 405,
            "message": "Method not allowed"
        },
    )

@app.post("/issue/add")
async def add_issue(request: Request):
    pass

if __name__ == '__main__':
    
    uvicorn.run("main:app", host=HOST, port=PORT,reload=True)