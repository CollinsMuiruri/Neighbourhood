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
    url(r'^new_business/$', views.new_business, name='new_business'),
    url(r'^business/details$', views.business_details, name='business_details'),
    url(r'^businesses/$', views.businesses, name='businesses'),
    url(r'^new_neighbourhood/$', views.new_neighbourhood, name='new_neighbourhood'),
    url(r'^neighbourhooders/$', views.neighbourhoods, name='neighbourhoods'),
    url(r'^contacts/$', views.chat, name='contacts'),
    url(r'^social_details/$', views.social_details, name='social'),
    url(r'^join/(\d+)', views.join, name='joinHood'),
    url(r'^exitHood/(\d+)', views.exitHood, name='exitHood'),
    # url(r'^chatty/$', views.chatty, name='chatty'),
    url(r'^lipapesa/$', views.error, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
