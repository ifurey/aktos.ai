from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
# Register your viewsets here
# router.register('endpoint', views.SomeViewSet)

urlpatterns = [
    path('', views.api_root, name='root'),
    path('v1/', include(router.urls)),
    # Add your API views here
] 