from django.urls import path
from .views import MessageCreate

urlpatterns = [
    path('', MessageCreate.as_view({'post': 'create'}), name='messages')
]
