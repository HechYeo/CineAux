from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class DisableBackButtonMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Prevent caching for all users
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        # Redirect to login page if the user is not authenticated and tries to access protected pages
        if not request.user.is_authenticated:
            # You can customize the redirect URL based on your needs
            if request.path != '/login/':  # Prevent redirect loop to login page
                return redirect('login')
        
        return response
