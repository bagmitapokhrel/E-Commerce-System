from django.shortcuts import redirect

#to check if user is logged in or not
def unathenticated_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_function

#give access to admin page if user request comes from staff is 1 otherwise give access to normal user page
def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_function
