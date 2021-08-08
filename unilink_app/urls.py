from django.urls import path
from . import views

app_name = "unilink_app"

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('c/<str:collection_link>', views.CollectionView.as_view(), name='collectionView'),
    path('edit_name/<str:collection_link>', views.EditCollectionName.as_view(), name='editname'),
    path('set_pass/<str:collection_link>', views.SetCollectionPassword.as_view(), name='setcollpass'),
    path('how_to_use', views.HowToUse.as_view(), name='howtouse'),
    path('aboutus', views.AboutUs.as_view(), name='aboutus'),
    path('switch_visibility/<str:collection_link>', views.SwitchVisibilty.as_view(), name='visi'),
]