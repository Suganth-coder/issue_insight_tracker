from pydantic import BaseModel, AfterValidator, BeforeValidator, ValidationError
from typing import Annotated, Optional

def is_valid_status(status: str):
    valid_status = ['open','triaged', 'in_progress', 'done']
    if status not in valid_status:
        raise ValueError(f"Invalid status '{status}'. Must be one of {valid_status}")
    
    return status

def is_valid_title(title: str):
    if title is None:
        return None
    
    title = title.strip()
    if title:
        title = title[0].upper() + title[1:]
    
    if len(title) < 3:
        raise ValueError("Title must be at least 3 characters long")
    
    return title

class AddIssue(BaseModel):
    title: Annotated[str, BeforeValidator(is_valid_title)]
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
