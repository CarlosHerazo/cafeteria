from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class CustomAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        usuario = request.session.get('usuario')
        if not usuario:
            if not request.path.startswith('/login') and not request.path.startswith('/register'):
                return redirect('login')