from django.urls import path
from . import views

app_name = 'api_app'

urlpatterns = [
    path('', views.index, name="api"),
    path('img-url-list/', views.imgUrlList, name="img-url-list"),
    path('user/', views.user, name="user"),
    path('user/<str:username_path>', views.user, name="user"),
    path('db-info', views.dbInfo, name="db-info"),
    path('send-mail', views.sendMail, name="send-mail"),
    path('run-test', views.runTest, name="run-test")
]