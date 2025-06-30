from django.urls import path
from .views import (
    HomeView, SubjectDetailView, CourseDetailView,
    CourseCreateView, CourseUpdateView, CourseDeleteView,
    ModuleDetailView, TopicDetailView, ContentDetailView, VideoDetailView, CoursesListView, RegisterView, TeacherView
)

app_name = 'course'


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('subject/<slug:slug>/', SubjectDetailView.as_view(), name='subject_detail'),

    path('courses/', CoursesListView.as_view(), name='courses_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/add/', CourseCreateView.as_view(), name='course_add'),
    path('course/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('module/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),

    path('about/', RegisterView.as_view(), name='about'),

    path('teacher', TeacherView.as_view(), name='teacher'),

    # Polymorphic content detail (text/video/image/file)
    path('content/<str:model_name>/<int:pk>/', ContentDetailView.as_view(), name='content_detail'),

]
