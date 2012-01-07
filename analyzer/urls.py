from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('analyzer.views',
    url(r'^$', 'index', name='index'),
    url(r'^statement/add/$', 'add_statement', name='add_statement'),
    url(r'^statement/(?P<id>\d+)/delete/$', 'delete_statement', name='delete_statement'),
    url(r'^purchases/$', 'purchases', name='purchases'),
    )
                       
          
