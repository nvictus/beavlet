from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Profile

from dropbox.client import DropboxClient, DropboxOAuth2Flow
DROPBOX_APP_KEY = settings.DROPBOX_APP_KEY
DROPBOX_APP_SECRET = settings.DROPBOX_APP_SECRET

def get_auth_flow(request):
    redirect_uri = request.build_absolute_uri(reverse(dropbox_auth_finish))
    return DropboxOAuth2Flow(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, 
        redirect_uri, request.session, 'dropbox-auth-csrf-token')

# Views
# -----
@login_required
def home(request):
    """
    Render personalized welcome page if user has already linked their dropbox.
    Otherwise, page provides option to link.

    """
    user = request.user
    try:
        access_token = user.profile.access_token
    except Profile.DoesNotExist:
        access_token = None

    real_name = None
    if access_token:
        client = DropboxClient(access_token)
        account_info = client.account_info()
        real_name = account_info["display_name"]

    return render(request, 'dropbox/index.html', {'real_name':real_name})

def dropbox_link(request):
    """
    Starts the Dropbox OAuth2 flow, which will redirect to dropbox-auth-finish.

    """
    # note: you can send GET data to the auth_finish callback
    flow = get_auth_flow(request)
    authorize_url = flow.start()
    return redirect(authorize_url)

@login_required
def dropbox_auth_finish(request):
    """
    Complete the OAuth2 process to link with user's Dropbox.

    """
    user = request.user
    try:
        flow = get_auth_flow(request)
        access_token, user_id, url_state = flow.finish(request.GET)

    except DropboxOAuth2Flow.BadRequestException, e:
        return HttpResponse(status=400)

    except DropboxOAuth2Flow.BadStateException, e:
        return HttpResponse(status=400)

    except DropboxOAuth2Flow.CsrfException, e:
        return HttpResponse(status=403)

    except DropboxOAuth2Flow.NotApprovedException, e:
        messages.add_message(request, messages.ERROR, 
            'Not approved?  Why not, bro?')
        return redirect('/dropbox/')

    except DropboxOAuth2Flow.ProviderException, e:
        messages.add_message(request, messages.ERROR, 
            'Auth error: ' + str(e))
        return HttpResponse(status=403)

    # attach a dropbox profile to the current session user
    Profile.objects.create(user=user, dropbox_id=user_id, 
        access_token=access_token)
    messages.add_message(request, messages.SUCCESS,
        "Your dropbox account was sucessfully linked!")
    return redirect('/dropbox/')

@login_required
def dropbox_unlink(request):
    """
    Delete the user's dropbox info from our db.

    """
    user = request.user
    try:
        user.profile.delete()
        messages.add_message(request, messages.SUCCESS,
            "Your dropbox account has been unlinked!")
    except Profile.DoesNotExist:
        pass
    return redirect('/dropbox/')


@login_required
def list_beavlets(request):
    user = request.user
    try:
        access_token = user.profile.access_token
    except Profile.DoesNotExist:
        messages.add_message(request, messages.ERROR,
            "Your dropbox account needs to be linked!")
        return redirect('/dropbox/')

    import os
    beavlet_root = u'/'
    ls = {}

    client = DropboxClient(access_token)
    resp = client.metadata(beavlet_root)
    if 'contents' in resp:
        for f in resp['contents']:
            path = f['path']
            name = os.path.basename(path)
            ls[name] = '/dropbox/render-beavlet/' + name

    return render(request, 'dropbox/list-beavlets.html',
        {'listing': ls})

@login_required
def render_beavlet(request, doc):
    user = request.user
    try:
        access_token = user.profile.access_token
    except Profile.DoesNotExist:
        message.add_message(request, messages.ERROR,
            "Your dropbox account needs to be linked!")
        return redirect('/dropbox/')

    client = DropboxClient(access_token)
    f, meta = client.get_file_and_metadata('/' + doc)
    s = f.read()
    from apps.nbviewer.views import render_raw_json_to_response
    return render_raw_json_to_response(request, s)














