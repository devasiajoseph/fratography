# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template.response import TemplateResponse
from app.forms import CreateUserForm, LoginForm, PasswordEmailForm
from app.utilities import reply_object, create_key, paginate
import simplejson
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
import datetime
from app.models import UserProfile, SocialAuth, Album, AlbumImage
from app.forms import PasswordResetForm, PasswordEmailForm, BookingForm,\
    VoteForm
from django.contrib.auth import authenticate, login
from django.core import serializers


def index(request):
    return render_to_response("kappa.html",
                              context_instance=RequestContext(request))


def home(request):
    """
    Home page after logging in
    """
    if request.user.is_authenticated():
        return render_to_response("home.html",
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login'))


def user_register(request):
    """
    Registration page
    """
    form = CreateUserForm()
    return render_to_response(
        "register.html",
        context_instance=RequestContext(request, {"user_form": form}))


def add_user(request):
    """
    Registration request handler
    """
    response = reply_object()
    form = CreateUserForm(request.POST)
    if form.is_valid():
        response = form.save_user()
        response["success_page"] = reverse('registration_success')
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def registration_success(request):
    return render_to_response('registration_success.html',
                              context_instance=RequestContext(request,
                {"activation_email": settings.EMAIL_VERIFICATION_REQUIRED}))


def user_login(request):
    """
    Login page
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    form = LoginForm(request=request)
    return render_to_response("login.html",
            context_instance=RequestContext(request,
                {"login_form": form}))


def login_user(request):
    """
    Login request handler
    """
    response = reply_object()
    form = LoginForm(request.POST, request=request)

    if form.is_valid():
        response["code"] = settings.APP_CODE["LOGIN"]
        response["next_view"] = reverse('home')
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))


def user_logout(request):
    """
    Logout request
    """
    # Logout function flushes all sessions.Save session variables to a local
    # variable for reuse
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def activate(request, verification_key):
    """
    New account activation function
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    user_profile = get_object_or_404(UserProfile,
                                     verification_key=verification_key)
    naive_date = user_profile.key_expires.replace(tzinfo=None)
    if naive_date < datetime.datetime.today():
        return render_to_response('expired.html',
                                  context_instance=RequestContext(request))
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    #remove activation key once account is activated
    user_profile.verification_key = ""
    user_profile.save()
    return render_to_response('activated.html',
                              context_instance=RequestContext(request))


def start_fbauth(request):
    """
    Starting point for facebook authentication
    """
    social_auth = SocialAuth(request=request)
    redirect_url = social_auth.facebook_step1()
    return HttpResponseRedirect(redirect_url)


def fbauth(request):
    """
    Redirect function after facebook authentication
    """
    social_auth = SocialAuth(request=request)
    social_auth.facebook_step2()
    return HttpResponseRedirect(reverse('home'))


def start_twauth(request):
    """
        The view function that initiates the entire handshake.
    """
    social_auth = SocialAuth(request=request)
    redirect_url = social_auth.twitter_step1()
    return HttpResponseRedirect(redirect_url)


def twauth(request):
    """
    Redirect function after twitter login
    """

    social_auth = SocialAuth(request=request)
    social_auth.twitter_step2()
    return HttpResponseRedirect(reverse('home'))


def start_googleauth(request):
    """
    Starting point for google authentication
    uses oauth2.0
    """
    social_auth = SocialAuth(request=request)
    redirect_url = social_auth.google_step1()
    return HttpResponseRedirect(redirect_url)


def googleauth(request):
    """
    Redirect after google auth
    """
    social_auth = SocialAuth(request=request)
    social_auth.google_step2()
    return HttpResponseRedirect(reverse('home'))


def password_reset(request):
    """
    Password reset step1
    """
    reset_form = PasswordEmailForm()

    return render_to_response('password_reset.html',
                                  context_instance=RequestContext(
            request, {"reset_form": reset_form}))


def password_reset_submit_email(request):
    response = reply_object()
    form = PasswordEmailForm(request.POST)
    if form.is_valid():
        response = form.send_reset_link()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))


def password_reset_form(request, verification_key):
    """
    Password reset form
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    user_profile = get_object_or_404(UserProfile,
                                     verification_key=verification_key)
    naive_date = user_profile.key_expires.replace(tzinfo=None)
    if naive_date < datetime.datetime.today():
        return render_to_response('expired.html',
                                  context_instance=RequestContext(request))

    user_account = user_profile.user
    temp_password = create_key(user_account.username, 2)
    user_account.set_password(temp_password)
    user_account.save()
    user = authenticate(username=user_account.username, password=temp_password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            return HttpResponse("This account is inactive.")
    #remove reset key
    user_profile.verification_key = ""
    user_profile.save()
    reset_form = PasswordResetForm()
    return render_to_response('password_reset_form.html',
                              context_instance=RequestContext(
            request, {"reset_form": reset_form}))


def password_reset_submit_password(request):
    response = reply_object()
    form = PasswordResetForm(request.POST, request=request)
    if form.is_valid():
        response = form.save_new_password()
        response["code"] = settings.APP_CODE["CALLBACK"]
        response["redirect"] = reverse('home')
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))


def calendar(request):
    form = BookingForm()
    return render_to_response('site_calendar.html',
                              context_instance=RequestContext(request,
                                                              {"form": form}))


def albums(request):
    return TemplateResponse(request, "albums.html", {})


def album_objects(request):
    page = int(request.GET["page"])
    count = int(request.GET["show"])
    pages = paginate(page, count)
    albums = {}
    albums["data"] = []
    for each_album in Album.objects.all()[pages["from"]:pages["to"]]:
        album_dict = {}
        album_dict["id"] = each_album.id
        album_dict["cover_photo"] = each_album.cover_photo
        album_dict["name"] = each_album.name
        albums["data"].append(album_dict)

    albums["total_count"] = Album.objects.count()
    return HttpResponse(simplejson.dumps(albums), mimetype="application/json")


def album_photos(request):
    page = int(request.GET["page"])
    count = int(request.GET["show"])
    pages = paginate(page, count)
    album_id = int(request.GET["album_id"])
    album = Album.objects.get(pk=album_id)
    album_photos = {}
    album_photos["data"] = []
    for each_photo in AlbumImage.objects.filter(album=album)[
        pages["from"]:pages["to"]]:
        photo_dict = {}
        photo_dict["id"] = each_photo.id
        photo_dict["thumbnail"] = each_photo.thumbnail
        photo_dict["display"] = each_photo.display
        album_photos["data"].append(photo_dict)

    album_photos["total_count"] = AlbumImage.objects.filter(
        album=album).count()
    return HttpResponse(simplejson.dumps(album_photos),
                        mimetype="application/json")

    
def vote(request):
    response = reply_object()
    form = VoteForm(request.POST, request=request)
    if form.is_valid():
        response = form.do_vote()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))
    
    
def test(request):
    """
    Test function
    """
    print "test"
    return HttpResponse("test")
