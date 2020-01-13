"""View decorators.

See also decorators provided by server-specific modules, such as
:func:`django_downloadview.nginx.x_accel_redirect`.

"""

from functools import wraps

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner


class DownloadDecorator(object):
    """View decorator factory to apply middleware to ``view_func``'s response.

    Middleware instance is built from ``middleware_factory`` with ``*args`` and
    ``**kwargs``. Middleware factory is typically a class, such as some
    :py:class:`django_downloadview.BaseDownloadMiddleware` subclass.

    Response is built from view, then the middleware's ``process_response``
    method is applied on response.

    """

    def __init__(self, middleware_factory):
        """Create a download view decorator."""
        self.middleware_factory = middleware_factory

    def __call__(self, view_func, *middleware_args, **middleware_kwargs):
        """Return ``view_func`` decorated with response middleware."""

        def decorated(request, *view_args, **view_kwargs):
            """Return view's response modified by middleware."""
            response = view_func(request, *view_args, **view_kwargs)
            middleware = self.middleware_factory(*middleware_args, **middleware_kwargs)
            return middleware.process_response(request, response)

        return decorated


def _signature_is_valid(request):
    """
    Validator that raises a PermissionDenied error on invalid and
    mismatching signatures.
    """

    signer = TimestampSigner()
    signature = request.GET.get("X-Signature")
    expiration = getattr(settings, "DOWNLOADVIEW_URL_EXPIRATION", None)

    try:
        signature_path = signer.unsign(signature, max_age=expiration)
    except SignatureExpired as e:
        raise PermissionDenied("Signature expired") from e
    except BadSignature as e:
        raise PermissionDenied("Signature invalid") from e
    except Exception as e:
        raise PermissionDenied("Signature error") from e

    if request.path != signature_path:
        raise PermissionDenied("Signature mismatch")


def signature_required(function):
    """
    Decorator that checks for X-Signature query parameter to authorize access to views.
    """

    @wraps(function)
    def decorator(request, *args, **kwargs):
        _signature_is_valid(request)
        return function(request, *args, **kwargs)

    return decorator
