# your_app/decorators.py
from django.http import Http404

def login_required_404(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("Page not found")
        return view_func(request, *args, **kwargs)
    return wrapper
