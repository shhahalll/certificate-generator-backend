from django.urls import path
from .views import GetCert, ListAll, LoginView, UploadTemplate

urlpatterns = [
    path('certificate/<int:state>/', GetCert.as_view(), name='get-certificate'),
    path('list/', ListAll.as_view(), name='list-all'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload-template/', UploadTemplate.as_view(), name='upload-template'),
]
