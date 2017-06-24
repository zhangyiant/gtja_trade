from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^buy/$', views.buy_view, name="buy_view"),
    url(r'^sell/$', views.sell_view, name="sell_view"),
    url(r'^noble-metal-buy/$', views.noble_metal_buy_view,
        name="noble_metal_buy_view"),
    url(r'^noble-metal-sell/$', views.noble_metal_sell_view,
        name="noble_metal_sell_view"),
    url(r'^stock_infos/$', views.stock_info_view, name="stock_info_view")
]
