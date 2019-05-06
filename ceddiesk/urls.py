from django.urls import include, path
from rest_framework import routers
from ceddiesk_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'advisers', views.AdviserViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'requests', views.RequestViewSet)
router.register(r'comments', views.CommentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path(r'api/', include('ceddiesk_app.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]