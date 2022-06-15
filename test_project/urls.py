from django.urls import re_path, include


urlpatterns = [
    re_path(r'^resigner_tests/', include('resigner_tests.urls')),
]