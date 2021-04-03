from django.urls import path
from . import views
urlpatterns = [
    path('pricing-table/',views.PricingTableView, name='pricing-table'),
    path('checkout/<int:id_p>',views.CheckoutPageView, name='checkout'),
    path('charge/<int:id_p>',views.Charge, name='charge'),
    path('free-sub/<int:id_p>',views.FreeSub, name='free-sub'),
]