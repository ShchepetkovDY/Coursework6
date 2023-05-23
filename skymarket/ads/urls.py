from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AdViewSet, CommentViewSet

ad_router = routers.SimpleRouter()
ad_router.register('ads', AdViewSet, basename='ads')

comment_router = routers.NestedSimpleRouter(ad_router, "ads", lookup='ads')
comment_router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path('', include(ad_router.urls)),
    path('', include(comment_router.urls)),

    path('login/', views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]

