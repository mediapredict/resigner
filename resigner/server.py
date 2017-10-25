from functools import wraps
import time

from django.http import Http404, HttpResponseBadRequest

from .models import ApiKey
from .utils import get_signature, get_settings_param, \
    SERVER_TIME_STAMP_KEY, SERVER_API_SIGNATURE_KEY, SERVER_API_KEY

def signed_req_required(view_func):

    def check_signature(request, *args, **kwargs):

        def identify_api_client():
            api_client = None

            if not SERVER_API_KEY in request.META.keys():
                return api_client

            client_identification = request.META[SERVER_API_KEY]
            try:
                api_client = ApiKey.objects.get(key=client_identification)
            except ApiKey.DoesNotExist:
                time.sleep(1) # rate limiting

            return api_client

        def is_time_stamp_valid():
            if not SERVER_TIME_STAMP_KEY in request.META.keys():
                return False
            received_times_stamp = request.META[SERVER_TIME_STAMP_KEY]

            max_delay = get_settings_param("RESIGNER_API_MAX_DELAY", 5*60)
            time_stamp_now = time.time()

            return (
                abs(time_stamp_now - float(received_times_stamp)) < max_delay
            )

        def is_signature_ok():
            if not SERVER_API_SIGNATURE_KEY in request.META.keys():
                return False
            api_signature = request.META[SERVER_API_SIGNATURE_KEY]

            try:
                time_stamp = request.META[SERVER_TIME_STAMP_KEY]
                url = request.build_absolute_uri()
                expected_signature = get_signature(
                    api_client.secret,
                    request.body.decode("utf-8"),
                    time_stamp,
                    url
                )

                if api_signature == expected_signature:
                    return True

            except:
                pass

            return False

        api_client = identify_api_client()
        if not api_client:
           return HttpResponseBadRequest("The API KEY used in this request does not exist")

        if is_time_stamp_valid() and is_signature_ok():
            return view_func(request, *args, **kwargs)
        else:
            raise Http404

    return wraps(view_func)(check_signature)
