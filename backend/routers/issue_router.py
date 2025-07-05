from fastapi import APIRouter,  Response, Request

from library.authentication import ClerkAuthentication

issue_router = APIRouter()

@issue_router.get("/test")
async def add_issue(request: Request):
    
    @ClerkAuthentication.authorize
    def logic(data):
        print(data)

    return logic({"issueID":"1234"},request)