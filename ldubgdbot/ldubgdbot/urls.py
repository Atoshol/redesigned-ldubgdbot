from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from ldubgdbot.api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'admins', views.AdminViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('api.urls'))
]
