from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import FoodView, GroupViewSet, UserCreateView, logout_view
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

router = DefaultRouter()
router.register(r'foods', FoodView)
router.register(r'groups', GroupViewSet)
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('userinfo/', views.get_user_info, name='user_info'),
    path('signup/', UserCreateView.as_view(), name='user_signup'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),
]


# path('api/user-permissions/', views.UserGroupPermissionView.as_view(), name='user-permissions'),