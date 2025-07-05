from fastapi import FastAPI, Response, Request
from routers.issue_router import issue_router
from routers.file_router import file_router

from library.authentication import ClerkAuthentication

app = FastAPI()

app.include_router(issue_router, prefix="/issue", tags=["issue"])
app.include_router(file_router, prefix="/attachment", tags=["File Attachment"])


