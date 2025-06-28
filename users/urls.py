from django.urls import path , include
from .views import CustomLoginView , CustomRegisterView , activate_account, CustomLogOutView
app_name = 'users'

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('logout/', CustomLogOutView.as_view(), name='logout'),

]