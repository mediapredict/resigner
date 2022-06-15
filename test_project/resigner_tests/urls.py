from django.urls import re_path

from .views import my_test_api_view

urlpatterns = [
    re_path(r'^my_test_api_url/', my_test_api_view, name="my_test_api"),
]
