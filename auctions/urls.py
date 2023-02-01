from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new",views.new, name="new"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:name>", views.category, name="category"),
    path("listings/<str:name>", views.listing, name="listing")
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
