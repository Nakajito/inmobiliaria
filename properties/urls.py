from django.urls import path

from . import views

app_name = "properties"

urlpatterns = [
    path("", views.listing, name="listing"),
    path("<slug:slug>/", views.detail, name="detail"),
]
