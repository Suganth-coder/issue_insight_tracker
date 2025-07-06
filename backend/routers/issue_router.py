from fastapi import APIRouter,  Response, Request
from schemas.issue_schema import AddIssue, UpdateIssue, DeleteIssue
from routers.websocket import send_message_to_clients

from library.authentication import ClerkAuthentication
from library.issues import IssueManagement

issue_router = APIRouter()
issue_management = IssueManagement()

@issue_router.post("/add")
async def add_issue(issue_data: AddIssue, request: Request):
    
    @ClerkAuthentication.authorize
    def logic(data):
        return issue_management.create_issue(data)

    issue_data = issue_data.model_dump()
    response = logic(issue_data,request)

    if response['code'] == 200:
        await send_message_to_clients("issue_updated")

    return response

@issue_router.get("/all")
async def get_issue( request: Request):

    @ClerkAuthentication.authorize
    def logic(data):
        return issue_management.get_issue(data)

    return logic({"get_all_issues":True}, request)


@issue_router.put("/{issue_id}")
async def update_issue(issue_id: str, issue_data: UpdateIssue, request: Request):
    issue_data = issue_data.model_dump()
    issue_data['issue_id'] = issue_id

    @ClerkAuthentication.authorize
    def logic(data):
        return issue_management.update_issue(data)

    response =  logic(issue_data, request)

    if response['code'] == 200:
        await send_message_to_clients("issue_updated")

    return response

@issue_router.delete("/{issue_id}") 
async def delete_issue(issue_id: str, request: Request):
    issue_data = DeleteIssue(issue_id=issue_id).model_dump()

    @ClerkAuthentication.authorize
    def logic(data):
        return issue_management.delete_issue(data)

    response = logic(issue_data, request)

    if response['code'] == 200:
        await send_message_to_clients("issue_updated")

    return response