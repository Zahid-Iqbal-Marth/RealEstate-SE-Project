from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='realestate-home'),
    path('contact/', views.contact, name='realestate-contact'),
    path('about/', views.about, name='realestate-about'),

    path('post-new/', views.CreatePostView, name='post-ad'),
    path('my-ads/', views.MyAds, name='my-ads'),
    path('view-all/', views.AllPropertiesView, name='view-all'),
    path('post-update/<int:id_p>/', views.UpdatePostView, name='post-update'),
    path('post-delete/<int:id_p>/', views.DeletePostView, name='post-delete'),
    path('post-detail/<int:id_p>/', views.DetailPostView, name='post-detail'),


    path('post-search', views.SearchView, name='search'),


    

]