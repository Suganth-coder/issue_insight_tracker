from pydantic import BaseModel, AfterValidator
from typing import Annotated, Optional

def is_valid_status(status: str):
    valid_status = ['open','triaged', 'in_progress', 'done']
    if status not in valid_status:
        raise ValueError(f"Invalid status '{status}'. Must be one of {valid_status}")
    
    return status
class AddIssue(BaseModel):
    title: str
    description: str
    s3_object_key: Optional[str] = None

class UpdateIssue(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Annotated[str, AfterValidator(is_valid_status)]] = None
    severity: Optional[str] = None
    s3_object_key: Optional[str] = None 


class DeleteIssue(BaseModel):
    issue_id: str
