from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('pastebin.views',
        url(r'^$', 'index', name='djpaste_index'),

        # blog home page
        url(r'^blog/', 'getPosts', name='blog_posts'),
        url(r'^(?P<selected_page>\d+)/?$', 'getPosts'),
        url(r'^\d{4}/\d{1,2}/(?P<postSlug>[-a-zA-Z0-9]+)/?$', 'getPost'),

        url(r'^help/$', TemplateView.as_view(template_name='djpaste/help.html'),
        									name='djpaste_help'),
        url(r'^paste/(?P<id>\d+)/$', 'paste_details', name='djpaste_paste_details'),
        url(r'^plain/(?P<id>\d+)/$', 'plain', name='djpaste_plain'),
        url(r'^html/(?P<id>\d+)/$', 'html', name='djpaste_html'),


)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    							{'document_root': settings.STATIC_ROOT}),
)
