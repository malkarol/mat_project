
from django.urls import path
from webapp import views


urlpatterns=[
    path('upload-weights/', views.upload_weights),
     path('upload-many/', views.upload_many),
]