from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class DisableBackButtonMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Apply cache-control headers to prevent caching of sensitive pages
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        # Prevent users from going back to the book_seats page after booking
        if request.path == '/book_seats/' and request.method == 'GET':
            # Check if the user has already completed the booking (using session flag)
            if 'booking_complete' in request.session:
                return redirect('booking_confirmation')  # Redirect to confirmation page if booking is completed

        # Redirect users to the login page if they try to access any page while logged out
        # This check ensures that after logging out, users cannot access protected pages
        if not request.user.is_authenticated:
            if request.path not in ['/login/', '/register/']:  # Don't redirect on login or register pages
                return redirect('login')

        return response
