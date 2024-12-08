from django.urls import path
from .views import FetchDealsView, FetchContactsView, AssociationView

urlpatterns = [
    path('deals/', FetchDealsView.as_view(), name='fetch-deals'),
    path('contacts/', FetchContactsView.as_view(), name='fetch-contacts'),
    path('associations/', AssociationView.as_view(), name='associations'),
]
