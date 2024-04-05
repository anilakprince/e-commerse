from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views  import UserViewSet
from .import views
router = DefaultRouter()
router.register(r'',UserViewSet)

urlpatterns = [
    path('login/',views.signin,name='signin'),
    path('logout/<int:id>',views.signout,name='signout'),
    path('',include(router.urls)),
]