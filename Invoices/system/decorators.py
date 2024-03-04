from django.http import HttpResponseRedirect
from functools import wraps


def is_user_login(view_func, login_path='/'):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Perform custom actions before the view function
        if 'user_token' not in request.session:
            return HttpResponseRedirect(login_path)
        # Call the original view function
        response = view_func(request, *args, **kwargs)
        return response
    return wrapper