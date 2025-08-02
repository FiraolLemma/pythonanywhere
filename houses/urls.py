# houses/urls.py
from django.urls import path
from . import views
# like and share functionality
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .views import like_house, share_house
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

app_name = 'houses'

urlpatterns = [
    path('', views.HouseListView.as_view(), name='house_list'),
    path('category/<slug:category_slug>/', views.HouseListView.as_view(), name='category_houses'),
    path('<int:pk>/', views.HouseDetailView.as_view(), name='house_detail'),
    path('create/', views.HouseCreateView.as_view(), name='house_create'),
    path('<int:pk>/update/', views.HouseUpdateView.as_view(), name='house_update'),
    path('<int:pk>/delete/', views.HouseDeleteView.as_view(), name='house_delete'),
  
    # Function-based views (alternative)
    # path('', views.house_list, name='house_list'),
    # path('<int:pk>/', views.house_detail, name='house_detail'),
    # path('create/', views.house_create, name='house_create'),
    # path('<int:pk>/update/', views.house_update, name='house_update'),
    # path('<int:pk>/delete/', views.house_delete, name='house_delete'),

    # like and share
    path('house/<int:house_id>/like/', views.like_house, name='like_house'),
    path('house/<int:house_id>/share/', views.share_house, name='share_house'),
]