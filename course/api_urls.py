from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course.auth_views import RegisterView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

from .api_views import (
    SubjectListCreateAPIView,
    SubjectRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView,
    CommentViewSet, CoursePutOnlyView
)

router = DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('subjects/', SubjectListCreateAPIView.as_view(), name='subject_list_create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroyAPIView.as_view(), name='subject_detail'),

    # path('courses/', CourseListCreateAPIView.as_view(), name='course_list_create'),
    # path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course_detail'),

    path('courses/<int:pk>/', CoursePutOnlyView.as_view(), name='course_put_only'),

    path('', include(router.urls)),

    path('token/login/', obtain_auth_token, name='api_token_login'),
    path('token/register/', RegisterView.as_view(), name='api_token_register'),
    path('token/logout/', LogoutView.as_view(), name='api_token_logout'),
]
