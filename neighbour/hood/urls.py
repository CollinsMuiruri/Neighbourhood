from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .views import RegisterUserView
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^register$', view=RegisterUserView.as_view(), name='register'),
    url(r'^index/$', views.chat, name='index'),
    url(r'^home/$', views.welcome, name='welcome'),
    url(r'^detail/(?P<image_id>\d+)', views.detail, name='detail'),
    url(r'^search', views.search_results, name='search_results'),
    url(r'^new/image/$', views.new_image, name='new-image'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^neighbourhood_details/$', views.neighbourhood_details, name='social'),
    url(r'^business/$', views.business, name='business'),
    url(r'^business/details$', views.business_details, name='business_details'),
    url(r'^lipapesa/$', views.error, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
