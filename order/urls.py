from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (BuyerAppCreateView, ViewBuyerApp, view_struc_drawings,dealer_view, vendor_quotations,
                    view_quotations, exterior_view, interior_view, order_form, add_order,
                    save_cart, view_container_orders,view_container_order_items, create_order_pdf,view_report_sap, view_arc_drawings, view_3d_model)


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='order/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('create/buyer/application',BuyerAppCreateView.as_view(), name="create-buyerapp"),
    
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
    path('order-form/', order_form, name='order-form'),

    path('add-order/', add_order, name='add-order'),
    # path('add-order/<int:pk>/', add_order, name='add-order'),

    # path('order-detail/', cart_detail, name='cart-detail'),
    path('save-order/', save_cart, name='save-cart'),
    path('container/orders', view_container_orders, name='view-container-orders'),
    path('container/order/items/<int:pk>/', view_container_order_items, name='view-container-order-items'),
    path('my/orders', view_container_order_items, name='my-orders'),
    path('order/pdf', create_order_pdf, name='order-pdf'),
]