from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ConfirmUserAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='confirm'),
]