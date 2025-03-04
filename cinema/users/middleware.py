from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class DisableBackButtonMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Apply cache-control headers to prevent caching of sensitive pages
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        # Redirect users to the login page if they try to access any page while logged out
        # This check ensures that after logging out, users cannot access protected pages
        if not request.user.is_authenticated:
            if request.path not in ['/login/', '/register/']:  # Don't redirect on login or register pages
                return redirect('login')

        return response
