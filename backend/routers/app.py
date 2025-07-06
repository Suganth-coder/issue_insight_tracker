from fastapi import FastAPI, Response, Request
from routers.issue_router import issue_router
from routers.file_router import file_router

from library.authentication import ClerkAuthentication
from library.authentication.user_role_management import UserRoleManagement

app = FastAPI()
user_management = UserRoleManagement()

app.include_router(issue_router, prefix="/issue", tags=["issue"])
app.include_router(file_router, prefix="/attachment", tags=["File Attachment"])


@app.get("/user/role")
async def add_issue(request: Request):
    
    @ClerkAuthentication.authorize
    def logic(data):
        return user_management.get_user_role(email=data['user_email'])


    return logic({},request)