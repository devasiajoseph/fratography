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
    url(r'^$', 'administrator.views.admin_dashboard', name='admin_dashboard'),
    url(r'^calendar', 'administrator.views.calendar', name='calendar'),
    url(r'^price/perhour', 'administrator.views.price_perhour',
        name='price_perhour'),
    url(r'^save/price/perhour', 'administrator.views.save_price_perhour',
        name='save_price_perhour'),
    url(r'^save/availability', 'administrator.views.save_availability',
        name='save_availability'),
)