from django.http import HttpResponse
from django.shortcuts import render
import json
from dropbox.client import DropboxClient

def index(request):
    if False:
        action = 'Link'
        href = '/redirect/dropbox'
        icon = 'icon-plus'
    else:
        action = 'Unlink'
        href = '/unlink/dropbox'
        icon = 'icon-minus'

    c = {
        'isDropboxConfigured': True,
        'isDropboxAuth': True,
        'link_action': action, 
        'link_href': href,
        'link_icon': icon,
    }

    return render(request, 'dillinger/index.html', c)

def fetch_md(request):
    pass

def fetch_html(request, direct=False):
    pass

def fetch_dropbox_file(request):
    user = request.user
    try:
        access_token = user.profile.access_token
    except Profile.DoesNotExist:
        messages.add_message(request, messages.ERROR,
            "Your dropbox account needs to be linked!")
        return redirect('/dropbox/')

    client = DropboxClient(access_token)
    path = request.GET['mdFile']
    resp = {'data': client.get_file(path).read()}
    return HttpResponse(json.dumps(resp))

def save_dropbox(request):
    pass

def import_dropbox(request):
    user = request.user
    try:
        access_token = user.profile.access_token
    except Profile.DoesNotExist:
        messages.add_message(request, messages.ERROR,
            "Your dropbox account needs to be linked!")
        return redirect('/dropbox/')

    client = DropboxClient(access_token)
    ls = client.search(u'/', u'.md')

    return HttpResponse(json.dumps(ls), 
        content_type="application/json")


