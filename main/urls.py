from django.urls import path
from .views import landing_page, home_view


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', home_view, name='home'),
]