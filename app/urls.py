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
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^login/$', 'app.views.user_login', name='login'),
    url(r'^login_user$', 'app.views.login_user', name='login_user'),
    url(r'^logout', 'app.views.user_logout', name='logout'),
    url(r'^register', 'app.views.user_register', name='register'),
    url(r'^add/user$', 'app.views.add_user'),
    url(r'^activate/(?P<verification_key>[0-9a-z]+)$', 'app.views.activate'),
    url(r'^registration/success$', 'app.views.registration_success',
        name='registration_success'),
    #Facebook urls
    url(r'^start/fbauth', 'app.views.start_fbauth', name='start_fbauth'),
    url(r'^fbauth', 'app.views.fbauth', name='fbauth'),
    #twitter urls
    url(r'^start/twauth', 'app.views.start_twauth', name='start_twauth'),
    url(r'^twauth', 'app.views.twauth', name='twauth'),
    #google urls
    url(r'^start/googleauth', 'app.views.start_googleauth',
        name='start_googleauth'),
    url(r'^oauth2callback', 'app.views.googleauth', name='googleauth'),
    #password reset
    url(r'^password/reset$', 'app.views.password_reset',
        name='password_reset'),
    url(r'^password/reset/submit/email$',
        'app.views.password_reset_submit_email',
        name='password_reset_submit_email'),
    url(r'^password/reset/form/(?P<verification_key>[0-9a-z]+)$',
        'app.views.password_reset_form',
        name='password_reset_form'),
    url(r'^password/reset/submit/password$',
        'app.views.password_reset_submit_password',
        name='password_reset_submit_password'),
    url(r'^calendar$', 'app.views.calendar', name='calendar'),
    url(r'^albums/$', 'app.views.albums', name='albums'),
    url(r'^album/objects$', 'app.views.album_objects', name='album_objects'),
    url(r'^album/photos$', 'app.views.album_photos', name='album_photos'),
    url(r'^vote$', 'app.views.vote', name='vote'),
    url(r'^calculate/price$', 'app.views.calculate_price', name='calculate_price'),
    url(r'^book/event$', 'app.views.book_event', name='book_event'),
    url(r'^payment$', 'app.views.payment', name='payment'),
    url(r'^contact/submit$', 'app.views.contact_submit', name='contact_submit'),
    url(r'^download$', 'app.views.download', name='download'),
    url(r'^search$', 'app.views.search', name='search'),
    url(r'^search/album$', 'app.views.search_album', name='search_album')
)