from django.conf.urls import include
from django.contrib.auth.urls import url
from . import views
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', login, {'template_name': 'shop/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'shop/home.html'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- for social Authentication
    url(r'^shop-by-aisle/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    url(r'^shop-by-aisle/$', views.CategoryView.as_view(), name='aisle')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # to serve files uploaded by a user during development

