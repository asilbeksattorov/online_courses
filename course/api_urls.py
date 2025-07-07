from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
]
