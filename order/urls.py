from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (OrderCreateView, ViewOrder, specialuser_ViewOrder, dealer_view,
        re_request_access, view_content)


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='order/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('order',OrderCreateView.as_view(), name="order"),
    
    url(r'^view-content/(?P<uidb64>[0-9A-Za-z_\-]+)/$',specialuser_ViewOrder, name="specialuser_ViewOrder"),
    
    path('view-content',view_content, name="specialuser_ViewOrder"),

    path('view-order/',ViewOrder.as_view(), name="view-order"),
    
    path('dealer/',dealer_view, name="dealer-view"),

    url(r'^request-for-access/(?P<uidb64>[0-9A-Za-z_\-]+)/$',re_request_access, name="re_access"),
]