from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('account/', views.account, name='account'),
    path('home/', views.home, name='home'),
    path('buy_order_market/', views.buy_order_market_view, name='buy_order_market'),
    path('sell_order_market/', views.sell_order_market_view, name='sell_order_market'),
    path('buy_order_limit/', views.buy_order_limit_view, name='buy_order_limit'),
    path('sell_order_limit/', views.sell_order_limit_view, name='sell_order_limit'),
    path('cancel_order/', views.cancel_order_view, name='cancel_order'),
    path('market_maker/', views.market_maker,name='market_maker'),
    path('stop_market/', views.stop_market,name='stop_market'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
