from django.shortcuts import redirect

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
