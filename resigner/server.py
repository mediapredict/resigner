import hashlib
from functools import wraps

from django.conf import settings
from django.core import signing
from django.http import Http404

from .models import ApiKey

def signed_req_required(api_secret_key_name):

    def _signed_req_required(view_func):

        def check_signature(request, *args, **kwargs):
            def data_hash():
                hash = hashlib.sha1()
                req_method = request.POST if request.method == 'POST' else request.GET
                hash.update(str(req_method.dict()))
                return hash.hexdigest()[:10]

            def is_signature_ok():
                api_signature = request.META["HTTP_X_API_SIGNATURE"]
                try:
                    api_secret_key = ApiKey.objects.get(key=api_secret_key_name).secret
                    x_api_key_args = {
                        "s": api_signature,
                        "key": api_secret_key + data_hash(),
                        "max_age": settings.API_MAX_DELAY,
                        }
                    if settings.X_API_KEY == signing.loads(**x_api_key_args):
                        return True

                except:
                    pass

                return False

            if "HTTP_X_API_SIGNATURE" in request.META.keys() and is_signature_ok():
                return view_func(request, *args, **kwargs)
            else:
                raise Http404

        return wraps(view_func)(check_signature)

    return _signed_req_required