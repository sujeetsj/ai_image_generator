from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('generate/', views.generate_images_view, name='generate_images'),
    path('task-status/<str:group_id>/', views.check_task_status, name='check_task_status'),
    path('show-images/', views.show_generated_images, name='show_generated_images'),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)