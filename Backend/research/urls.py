from django.urls import path
from .views import seedbed_list, seedbed_detail

urlpatterns = [
    path("api/seedbeds/", seedbed_list, name="seedbed_list"),
    path("api/seedbeds/<int:seedbed_id>/", seedbed_detail, name="seedbed_detail"),
]