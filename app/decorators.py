from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from app.utilities import reply_object
from functools import wraps
import simplejson
from django.utils.decorators import available_attrs


def check_access(request, permission):
    """
    Checks defined access
    """
    access_parameters = reply_object()
    access_parameters["redirect_url"] = "access_denied"
    access_parameters["allow_access"] = False
    if not request.user.is_authenticated():
        access_parameters["redirect_url"] = "login"
        return access_parameters
    if permission == "user":
        access_parameters["allow_access"] = True
        return access_parameters
    if permission == "admin":
        me = request.user
        if me.is_superuser:
            access_parameters["allow_access"] = True
    if permission == "client":
        me = request.user
        if me.is_staff or me.is_superuser:
            access_parameters["allow_access"] = True

        return access_parameters

    return access_parameters


def post_required(view_func):
    """
    Decorator for views that checks that data is submitted to the view
    """
    def _checkpost(request, *args, **kwargs):
        """
        Checks for post data
        """
        response_object = {}
        if request.method == "POST":
            return view_func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                response_object["code"] = settings.\
                            APP_CODE["INVALID REQUEST"]
                return HttpResponse(simplejson.dumps(response_object))
            else:
                return HttpResponseRedirect(
                    reverse("invalid_request"))
    return wraps(view_func)(_checkpost)


def tag_processor(view_func):
    """
    Decorator for views has tag handling
    """
    def _check_tag_query(request, *args, **kwargs):
        """
        checks tag queries
        """
        if "addtag" in request.GET:
            return HttpResponseRedirect("/news/tags/?addtag=" + \
                request.GET["addtag"])
        else:
            return view_func(request, *args, **kwargs)

    return wraps(view_func)(_check_tag_query)


def access_required(permission, next_view=None):
    """
    Checks user access to a particular view
    Redirects to login if a page is requested
    Adds access denied code if ajax request
    """
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            access_parameters = check_access(request, permission)
            if access_parameters["allow_access"]:
                return func(request, *args, **kwargs)
            else:
                if request.is_ajax():
                    access_parameters["code"] = settings.\
                            APP_CODE["ACCESS DENIED"]
                    access_parameters["success"] = False
                    return HttpResponse(simplejson.dumps(access_parameters))
                else:
                    request.session['next_view'] = request.get_full_path()
                    return HttpResponseRedirect(
                        reverse(access_parameters["redirect_url"]))

        return wraps(func)(inner_decorator)

    return decorator


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(login_url or settings.LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator
