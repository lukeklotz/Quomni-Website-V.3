from django.contrib import admin
from django.urls import path, include
from qsite import views
from django.conf import settings
from django.conf.urls.static import static
from qsite.views import (CreateCheckoutSessionView, 
                         ProductLandingPageView)
                        

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('work.html/', views.work, name='work'),
    path('shop.html/', views.shop, name='shop'),
    path('cart.html/', views.cart, name='cart'),
    path('about.html/', views.about, name='about'),
    path('shop.html/details/<int:id>/', views.details, name='details'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    
    #Handle payment
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    
    #Payment complete/failed
    #path('paymentCompleted.html/', views.paymentCompletedView, name="completed"),
    #path('paymentFailed.html/', views.paymentFailedView, name="failed"),
]

# Serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)