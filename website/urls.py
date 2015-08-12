from django.conf.urls import include, url
from django.contrib import admin
from blog import views as blog_views
urlpatterns = [
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', blog_views.posts),
    url(r'^register/$', blog_views.register),
    url(r'^login/$', blog_views.login),
    url(r'^logout/$', blog_views.logout),
    url(r'^add-post/$', blog_views.add_post),
    url(r'^search/(?P<type_request>(\w+))/(?P<search_request>(\w+))$', blog_views.search),
    url(r'^(?P<username>(\w+))/$', blog_views.posts),
    url(r'^(?P<username>(\w+))/post(?P<post_id>[0-9]+)/$', blog_views.post),
]




























