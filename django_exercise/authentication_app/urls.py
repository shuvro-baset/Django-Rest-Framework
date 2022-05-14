from django.urls import path
from . import views

urlpatterns = [
    path('user/registration', view=views.UserRegisterView.as_view(), name='signup'),
    path('signin', view=views.ObtainAuthToken.as_view(), name='signin'),
    path('user/<int:user_id>', view=views.UserInfoView.as_view(), name='user_info'),
    path('signout', view=views.Signout.as_view(), name='signout'),
]