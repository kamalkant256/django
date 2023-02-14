from django.urls import path,include

from Account.views import Registration

urlpatterns = [
    path('registration/',Registration.as_view(),name="registration")
]
