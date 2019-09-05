from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (OrderCreateView, ViewOrder, view_content)


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='order/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('order',OrderCreateView.as_view(), name="order"),
    
    path('view-content',view_content, name="specialuser_ViewOrder"),

    path('view-order/',ViewOrder.as_view(), name="view-order"),
]