[![travis ci](https://travis-ci.org/mediapredict/resigner.png)](https://travis-ci.org/mediapredict/resigner)

# Resigner doc

## What it does
Signes API requests: each _client_ is identified by its key and granted access by a secret.
(no secret transmitted over to _server_ - used only to sign a request)

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

@signed_req_required
def my_api_view(request):
    resp = {"result": "this API has been protected with secret key"}
    return JsonResponse(resp)
```

Add through admin:
* in `ApiKeys`: _MY_API_KEY_ (key, used to identify a client) and _my_secret_key_ (secret, used to get access)

You may use auto generated or provide specific value.


### Client

```python
from resigner.client import post_signed, get_signed

res = post_signed(
    "http://mysite/api_url", {"some": "data_we_want_to_transmit"}, "my_client_key", "my_secret_key"
)

if res.status_code == 200:
    print "went good!"
else:
    print "error HTTP status_code:{0}".format(res.status_code)
...
```

In the case of connecting to Knitting Factory

```python
KF_URL = 'https://knittingfactory.herokuapp.com'

api_url = "{0}/explorer/api/search".format(settings.KF_URL)
request_data = {
    "q" : 
    '''
    "your_daffodil" = "one long string"
    ''',
    "flat" = False, # True will return kfid only
}
res = post_signed(api_url,
                         request_data,
                         settings.KF_API_KEY,
                         settings.KF_SECRET)
                       

```

`res.json()` will access the data dictionary

Make sure _MY_API_KEY_ and _MY_TEST_CLIENT_ have been added in the server's DB as explained above.
