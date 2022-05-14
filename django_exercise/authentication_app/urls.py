from django.urls import path
from . import views

urlpatterns = [
    path('user/registration', view=views.UserRegisterView.as_view(), name='signup'),
    path('signin', view=views.ObtainAuthToken.as_view(), name='signin'),
    path('signout', view=views.Signout.as_view(), name='signout'),
]
