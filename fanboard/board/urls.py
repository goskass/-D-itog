from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from .views import AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView, PrivateResponseListView, \
    AdSearchView, CreateResponseView

urlpatterns = [
                  path('board/', AdListView.as_view(), name='ad_list'),
                  path('board/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
                  path('board/create/', AdCreateView.as_view(), name='ad_create'),
                  path('board/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_update'),
                  path('board/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
                  path('board/<int:ad_id>/response/', CreateResponseView.as_view(), name='create_response'),
                  path('responses/', PrivateResponseListView.as_view(), name='private_responses'),
                  path('search/', AdSearchView.as_view(), name='ad_search'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

