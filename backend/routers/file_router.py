from fastapi import APIRouter,  Response, Request

from library.authentication import ClerkAuthentication

file_router = APIRouter()