import os

from fastapi import Request

from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions

from dotenv import load_dotenv

load_dotenv()

class ClerkAuthentication:
    def authorize(func):
        def wrapper(data, request):
            
            is_authorized = ClerkAuthentication.is_signed_in(request)

            return func(data) if is_authorized else 401
        
        return wrapper
    
    def is_signed_in(request: Request):

        clerk = Clerk(bearer_auth=os.getenv('CLERK_SECRET_KEY'))
        request_state = clerk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[''],

            )
        )
        return request_state.is_signed_in