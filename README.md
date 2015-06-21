[![travis ci](https://travis-ci.org/mediapredict/resigner.png)](https://travis-ci.org/mediapredict/resigner)

# Resigner doc

## How to install

```
pip install git+git://github.com/mediapredict/resigner.git
```

## Configuration

In settings.py:

```python

INSTALLED_APPS = (
    ...
    'resigner',
    ...
)
```

Optional

```python
RESIGNER_API_MAX_DELAY = 30 # max delay in seconds (default 5*60 seconds)
```

## Usage (in progress)

### Server

```python
from django.http import JsonResponse

from resigner.server import signed_req_required

@signed_req_required("MY_API_KEY")
def my_api_view(request):
    resp = {"result": "this API has been protected with secret key"}
    return JsonResponse(resp)
```

Add through admin:
* in `ApiKeys` (this identifies the API): _MY_API_KEY_ (key) and _my_secret_key_ (secret)
* in `ApiClients` (this identifies the client): _MY_TEST_CLIENT_ (name) _and my_client_key_ (key)


### Client


```python
...
res = post_signed(
    "http://mysite/api_url", {"key": "val"}, "my_client_key", "my_secret_key"
)

if res.status_code == 200:
    print "went good!"
else:
    print "error HTTP status_code:{0}".format(res.status_code)
...
```

Make sure _MY_API_KEY_ and _MY_TEST_CLIENT_ have been added in the server's DB as explained above.