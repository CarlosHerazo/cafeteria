from django.urls import path
from cafe_app import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.login_cafe, name="login"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)