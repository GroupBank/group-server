""" Module contains a set of decorators for the views """

from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_POST

import common.crypto.ec_secp256k1 as crypto


@require_POST
def post_parameters(view):
    """
    Decorator for all views.

    Extracts from a POST request the three parameters included in all messages/requests:
    *author*, *payload*, and *signature*. It passes these parameters as arguments to the view,
    along with the original request.

    It responds with a bad request if one of the parameters is missing from the request.
    """

    @wraps(view)
    def wrapper(request):

        try:
            author = request.POST['author']
            payload = request.POST['payload']
            signature = request.POST['signature']
        except KeyError:
            return HttpResponseBadRequest("Malformed request: request is missing a parameter.")

        # Call the view outside of the try/except to avoid unexpected results if the
        # view raises a KeyError
        return view(request, author, payload, signature)

    return wrapper


def authenticate(view):
    """
    Decorator for all views.

    Authenticates the request. It verifies if the signature for the payload corresponds to the
    author's key.

    It responds with a Forbidden error if the author key is not valid or if the signature is not
    verified.
    """

    @wraps(view)
    def wrapper(request, author, payload, signature):
        try:
            crypto.verify(author, signature, payload)
        except crypto.InvalidSignature:
            return HttpResponseForbidden("Authentication failed: signature was not validated.")
        except crypto.InvalidKey:
            return HttpResponseForbidden("Authentication failed: key is invalid.")

        # Call the view outside of the try/except to avoid unexpected results if the
        # view raises a and InvalidSignature or InvalidKey
        return view(request, author, payload, signature)

    return wrapper
