import settings

from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^media_main/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)

# CORE
urlpatterns += patterns('dollashaka',
    (r'^$', 'core.views.index'),
    url(r'^create_account/$', 'core.views.create_account', name="create_account"),
    url(r'^login/$', 'core.views.login_user', name="login"),
    url(r'^logout/$', 'core.views.logout_user', name="logout"),
)

# fromfile
## TODO: Add me later
