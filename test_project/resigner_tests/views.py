from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from resigner.server import signed_req_required

@signed_req_required("MY_API_KEY")
@csrf_exempt
def my_test_api_view(request):
    is_post = (request.method == 'POST')
    req = request.POST if is_post else request.GET
    test_data = req.get("MY_TEST_DATA", "")

    result = "test ok" if test_data or not is_post else "no data received"

    return JsonResponse({"result":result})