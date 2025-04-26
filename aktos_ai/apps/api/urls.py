from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views.collection_agency import CollectionAgencyViewSet
from .views.client import ClientViewSet
from .views.customer import CustomerViewSet
from .views.account import AccountViewSet
from .views.csv_upload import CSVUploadViewSet

app_name = 'api'

router = DefaultRouter()
router.register('collection-agencies', CollectionAgencyViewSet)
router.register('clients', ClientViewSet)
router.register('customers', CustomerViewSet)
router.register('accounts', AccountViewSet)
router.register('csv-upload', CSVUploadViewSet, basename='csv-upload')

urlpatterns = [
    path('', views.api_root, name='root'),
    path('v1/', include(router.urls)),
    # Add your API views here
] 