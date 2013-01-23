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
    url(r'^remove/availability', 'administrator.views.remove_availability',
        name='remove_availability'),
    url(r'^available/time$', 'administrator.views.available_time',
        name='available_time'),
    url(r'^album$', 'administrator.views.album',
        name='album'),
    url(r'^album/save$', 'administrator.views.album_save',
        name='album_save'),
    url(r'^album/image$',
        'administrator.views.album_image',
        name='album_image'),
    url(r'^album/image/delete$',
        'administrator.views.album_image_delete',
        name='album_image_delete'),
    url(r'^album/edit/(?P<album_id>[0-9]+)$', 'administrator.views.album_edit',
        name='album_edit'),
    url(r'^album/list/(?P<page>[0-9]+)$', 'administrator.views.album_list',
        name='album_list'),
    url(r'^album/delete$', 'administrator.views.album_delete',
        name='album_delete'),
    url(r'^get/album/images/(?P<album_id>[0-9]+)$',
        'administrator.views.get_album_images',
        name='get_album_images'),
    url(r'^album/category$', 'administrator.views.album_category'),
    url(r'^album/category/save$', 'administrator.views.album_category_save'),
    url(r'^album/category/get$', 'administrator.views.album_category_get'),
    url(r'^album/category/delete$', 'administrator.views.album_category_delete'),
    url(r'^album/category/sub$', 'administrator.views.album_category_sub'),
    url(r'^reset/vote$', 'administrator.views.reset_vote'),
    url(r'^reset/vote/submit$', 'administrator.views.reset_vote_submit'),
    url(r'^generic-mod-list/(?P<model_name>[0-9a-z]+)$',
        'administrator.views.generic_mod_list'),
    url(r'^generic-mod-action/(?P<model_name>[0-9a-z]+)$',
        'administrator.views.generic_mod_action'),
    url(r'^generic-mod-get/(?P<model_name>[0-9a-z]+)$',
        'administrator.views.generic_mod_get'),
    
)
