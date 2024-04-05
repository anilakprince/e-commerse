from django.urls import path, include
from .import views
from .views import PaymentAPIView
urlpatterns = [
path('gettoken/<str:id>/<str:token>/',views.generate_token, name="token.generate"),
path('process/<str:id>/<str:token>/',views.process_payment, name="payment.process"),
path('',PaymentAPIView.as_view(), name="payment"),
]