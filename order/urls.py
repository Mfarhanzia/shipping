from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (add_order,ViewBuyerApp, view_struc_drawings,dealer_view, vendor_quotations,
                    view_quotations, exterior_view, interior_view,
                    view_container_orders,view_container_order_items, view_report_sap, view_arc_drawings, view_3d_model, OrderForm)
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='order/login.html',redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('view/structural-drawings',view_struc_drawings, name="struc-drawings"),
    path('view/architectural-drawings',view_arc_drawings, name="arc-drawings"),
    path('view/reportsap', view_report_sap, name="report-sap"),
    path('3d/model', view_3d_model, name='model-3d'),

    path('buyer/applications',ViewBuyerApp.as_view(), name="buyer-app"),

    path('dealer/',dealer_view, name="dealer-view"),
    path('quotation/',vendor_quotations, name="vendor-quotation"),
    path('view/quotation/',view_quotations, name="view-quotation"),
    
    path('interior-view/', interior_view, name='interior-view'),
    path('exterior-view/', exterior_view, name='exterior-view'),

    path('add-order/', add_order, name='add-order'),

    path('order-form/',OrderForm.as_view(condition_dict={'5': OrderForm.check_user_authentication}), name='order-form'),

    path('container/orders', view_container_orders, name='view-container-orders'), #for admin
    path('container/order/items/<int:pk>/', view_container_order_items, name='view-container-order-items'),
    path('my/orders', view_container_order_items, name='my-orders'),# for users history
]