"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers
from django.conf.urls import include

schema_view = get_swagger_view(title='fAIr API') # provides configuration for swagger

router = routers.DefaultRouter()
router.register(r'dataset', DatasetViewSet) # gets crud operation for the model dataset
router.register(r'aoi', AOIViewSet) # gets crud operation for the model dataset
router.register(r'label', LabelViewSet) # gets crud operation for the model dataset

urlpatterns = [
    path('',schema_view), # for the swagger
    path('api/v1/auth/', include('login.urls')), # add auth urls
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)), # adding all the api to version 1 project is in development
    path('api/v1/fetch-raw/<int:aoi_id>/', RawdataApiView.as_view()),
    path('api/v1/dataset_image/build/', image_download_api),
    path('api/v1/download/<int:dataset_id>/', download_training_data),



]
