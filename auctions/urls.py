from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path('watchlist', views.watchlist, name='watchlist'),
    path("<str:listing_id>/update_watchlist", views.update_watchlist, name='update_watchlist'),
    path("categories", views.categories, name='categories'),
    path("categories/<str:category_id>", views.category, name='category'),
    path("<str:listing_id>/bid", views.bid, name='bid'),
    path("<str:listing_id>/comment", views.comment, name='comment')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
