from django.urls import path

from . import views

app_name = 'network'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('network/', views.NetworkList.as_view(), name='network_list'),
    path('network/create', views.NetworkCreate.as_view(), name='network_create'),
    path('network/<int:pk>/', views.NetworkDetail.as_view(), name='network_detail'),
    path('network/<int:pk>/delete/', views.NetworkDelete.as_view(), name='network_delete'),
    path('network/<int:pk>/host/create', views.HostCreate.as_view(), name='host_create'),
]
