from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wish_items$', views.wish_items),
    url(r'^add$', views.add), 
    url(r'^wish_items/add$', views.add),
    url(r'^create$', views.create),
    url(r'^clear$', views.clear),
    url(r'^add_wishlist/(?P<wishlistid>\d+)$', views.add_wishlist),
    url(r'^delete/(?P<wishlistid>\d+)$', views.delete),
    url(r'^remove/(?P<wishlistid>\d+)$', views.remove),
    url(r'^item/(?P<wishlistid>\d+)$', views.item),



    
]