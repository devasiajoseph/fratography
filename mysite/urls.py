from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reg.views.home', name='home'),
    # url(r'^reg/', include('reg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.index', name='index'),
    url(r'^app/', include('app.urls')),
    #administrator
    url(r'^admin/', include('administrator.urls')),
    #test url
    url(r'^test$', 'app.views.test', name='test'),
    url(r'^contact$', 'app.views.contact', name="contact"),
    url(r'^terms$', 'django.views.generic.simple.direct_to_template',
        {'template': 'terms.html',
         'extra_context':{'page_title':'Terms and conditions', "terms":"active"}}),
    #albums
    url(r'^album/$', 'app.views.album', name='album'),
    url(r'^frattiest/(?P<order>[0-9a-zA-Z ]+)$', 'app.views.frattiest_view',
        name='frattiest_view'),
    url(r'^(?P<college_name>[0-9a-zA-Z ]+)$', 'app.views.college_view',
        name='college_view'),
    url(r'^org/(?P<subcategory_name>[0-9a-zA-Z ]+)$',
        'app.views.subcategory_view', name='subcategory_view'),
)
