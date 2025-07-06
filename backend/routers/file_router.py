from fastapi import APIRouter,  Request, File, UploadFile
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

from library.authentication import ClerkAuthentication
from library.object_storage import S3Storage

file_router = APIRouter()
s3_storage = S3Storage()


@file_router.post("/upload")
async def upload_attachment(request: Request, attachment: UploadFile = File(...),):

    file_content = await attachment.read()
    data = {"attachment": attachment, "file_content": file_content, 
            "role":"reporter","user_id":"test_user_1"}    
    
    return s3_storage.upload_attachment(data)
        
@file_router.get("/{filename}")
async def get_attachment(filename: str):
    data = {'filename':filename, 'role': 'reporter', 'user_id': 'test_user_1'}
    result = s3_storage.get_attachment(data)

    if result != 404:
        return StreamingResponse(result["Body"], media_type="application/octet-stream", headers={"Content-Disposition": f"attachment: filename={filename}"})

@file_router.delete("/{filename}")
async def delete_attachment(filename: str):
    data = {'filename':filename, 'role': 'admin', 'user_id': 'test_user_1'}
    return s3_storage.delete_attachment(data)