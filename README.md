[![travis ci](https://travis-ci.org/mediapredict/resigner.png)](https://travis-ci.org/mediapredict/resigner)

## How to install

```
pip install git+git://github.com/mediapredict/resigner.git
```

## Configuration

In settings.py:

```python

RESIGNER_X_API_KEY = "some_x_api_key"

INSTALLED_APPS = (
 ...
    'resigner',
 ...
)
```

Optional

```python
RESIGNER_API_MAX_DELAY = 1 # max delay in seconds
```

## Usage (in progress)

Server
------
```python
from django.http import JsonResponse

from resigner.server import signed_req_required

@signed_req_required("MY_API_KEY")
def my_api_view(request):
    resp = {"result": "this API has been protected with secret key"}
    return JsonResponse(resp)
```

Add MY_API_KEY (key) and my_secret_key (secret) through admin/ApiKeys.


Client
------

```python
...
res = post_signed(
    "http://mysite/api_url", {"key": "val"}, settings.RESIGNER_X_API_KEY, "my_secret_key"
)
...
```

Make sure _MY_API_KEY_ has been added as explained above.