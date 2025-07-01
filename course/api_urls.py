from django.urls import path
from .api_views import (
    SubjectListCreateAPIView,
    SubjectRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('subjects/', SubjectListCreateAPIView.as_view(), name='subject_list_create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroyAPIView.as_view(), name='subject_detail'),

    path('courses/', CourseListCreateAPIView.as_view(), name='course_list_create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course_detail'),
]
