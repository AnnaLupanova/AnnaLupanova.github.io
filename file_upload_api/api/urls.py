from .views import View, Upload
from django.urls import path

urlpatterns = [
    path('files/', View.as_view(), name='files'),
    path('upload/', Upload.as_view(), name='upload')

]
