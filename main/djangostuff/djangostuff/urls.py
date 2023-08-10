from django.contrib import admin
from django.urls import path
from qsite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('work.html/', views.work, name='work'),
    path('shop.html/', views.shop, name='shop'),
    path('cart.html/', views.cart, name='cart'),
    path('checkout.html/', views.checkout, name='checkout'),
    path('about.html/', views.about, name='about'),
    path('shop.html/details/<int:id>/', views.details, name='details'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('index.html', views.send_email, name='send_email'),
]

# Serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)