from django.conf.urls import *

from .views import my_test_api_view

urlpatterns = [
    url(r'^my_test_api_url/', my_test_api_view, name="my_test_api"),
]
