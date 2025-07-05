import os

from fastapi import Request
from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
from dotenv import load_dotenv

from library.authentication.user_role_management import UserRoleManagement
load_dotenv()

class ClerkAuthentication:
    def authorize(func):
        def wrapper(data, request):
            
            clerk_data = ClerkAuthentication.is_signed_in(request)
            is_authorized = clerk_data.get('is_signed_in', False)

            if is_authorized:

                data['user_email'] = clerk_data['payload']['user_email']
                data['user_id'] = clerk_data['payload']['user_id']

                print(clerk_data['payload']['user_email'])
    
                # Get the user role based on email
                user_management = UserRoleManagement()
                user_role = user_management.get_user_role(email=data['user_email'])

                if user_role == 404:
                    user_management.add_user_role(
                        user_id=data['user_id'],
                        email=data['user_email']
                    )

            return func(data) if is_authorized else 401
        
        return wrapper
    
    def is_signed_in(request: Request):

        clerk = Clerk(bearer_auth=os.getenv('CLERK_SECRET_KEY'))
        request_state = clerk.authenticate_request(
            request,
            AuthenticateRequestOptions(
            )
        )

        payload = request_state.payload

        if request_state.is_signed_in and request_state.payload:
            return {'is_signed_in':request_state.is_signed_in, 'payload':payload}
        
        else:
            return {'is_signed_in':False, 'payload':None}