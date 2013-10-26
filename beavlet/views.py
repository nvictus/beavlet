from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import os
import re
import json

import requests
from requests.exceptions import RequestException, Timeout

from IPython.nbformat import current as nbformat
from IPython.nbconvert.exporters import HTMLExporter
from IPython.config import Config

# Instantiate and configure the exporter
config = Config()
config.HTMLExporter.template_file = 'basic'
config.NbconvertApp.fileext = 'html'
config.CSSHTMLHeaderTransformer.enabled = False
# don't strip the files prefix - we use it for redirects
config.Exporter.filters = {'strip_files_prefix': lambda s: s}
html_exporter = HTMLExporter(config=config)

class NbFormatError(Exception):
    pass

def four_hundred(request=None):
    if request is None:
        return HttpResponse(render_to_string("400.html"), status=400)
    return render(request, "400.html", status=400)

def four_o_four(request=None):
    if request is None:
        return HttpResponse(render_to_string("404.html"), status=404)
    return render(request, "404.html", status=404)

def five_hundred(request=None):
    if request is None:
        return HttpResponse(render_to_string("500.html"), status=500)
    return render(request, "500.html", status=500)






# Views
# =====

def hello(request):
    response = render(request, 'index.html')
    return response

def faq(request):
    return render(request, 'faq.md')

@csrf_exempt
def create(request, value=None):
    if request.method == 'POST':
        value = request.POST['gistnorurl'] #form entry

    gist = re.search(r'^https?://gist.github.com/(\w+/)?([a-f0-9]+)$', value)
    if re.match('^[a-f0-9]+$', value):
        response = redirect('/'+value)
    elif gist:
        response = redirect('/'+gist.group(2))
    elif value.startswith('https://'):
        response = redirect('/urls/'+value[8:])
    elif value.startswith('http://'):
        response = redirect('/url/'+value[7:])
    else: # assume http url
        response = redirect('/url/'+value) 

    return response

# caching not implemented yet #@cache.memoize(10*minutes)
def fetch_and_render_url(request, url, https=False):
    # 1. Fetch
    url = ('https://' + url) if https else ('http://' + url)
    try:
        r = cached_get_request(url)
    except RequestException:
        if '/files/' in url:
            new_url = url.replace('/files/', '/', 1) 
            return redirect(new_url)
        else:
            return five_hundred(request)
    if not r.ok:
        if r.status_code == 404:
            return four_o_four()
        else:
            return four_hundred()
    # 2. Render
    try:
        nb = parse_json(r.content)
        name, theme, body = render_nb(nb, url)
    except NbFormatError:
        return four_hundred(request)
    context = {'download_url': url,
               'download_name': name,
               'css_theme': theme,
               'mathjax_conf': None,
               'body': body }  
    return render(request, 'notebook.html', context) 

def fetch_and_render_gist(request, id=None, subfile=None):
    """Fetch and render a post from the Github API"""
    #1. Fetch
    try:
        r = github_api_request('gists/{}'.format(id))
    except RequestException:
        return five_hundred(request)
    if not r.ok:
        if r.status_code == 404:
            return four_o_four(request)
        else:
            return four_hundred(request)
    try:
        decoded = r.json().copy()
        files = decoded['files'].values()
        if subfile:
            files = [f for f in files if f['filename'] == subfile]
    except Exception:
        return five_hundred(request)
    #2. Render
    if len(files) == 1:
        try:
            nb = parse_json(files[0]['content'])
        except NbFormatError:
            return four_hundred(request)
        name, theme, body = render_nb(nb, files[0]['raw_url'])
        context = {'download_url': id,
                   'download_name': name,
                   'css_theme': theme,
                   'mathjax_conf': None,
                   'body': body }      
        response = render(request, 'notebook.html', context)
    else:
        entries = []
        for file in files :
            entry = {}
            entry['path'] = file['filename']
            entry['url'] = '/%s/%s' % (id, file['filename'])
            entries.append(entry)
        response = render(request, 'gistlist.html', {'entries': entries})
    return response


# def popular(request):
#     entries = [{'url':y.url, 'count':x} 
#                for x, y in stats.most_accessed(count=20)]
#     return render(request, 'popular.html', {'entries':entries})

# =====











# caching not implemented yet #@cache.memoize()
def cached_get_request(url):
    return requests.get(url, timeout=8)

def github_api_request(url):
    return requests.get('https://api.github.com/%s' % url) # params=app.config['GITHUB'])

def parse_json(content):
    try :
        nb = nbformat.reads_json(content)
    except ValueError:
        raise NbFormatError('Error reading json notebook')
    return nb

def render_nb(nb, url):
    # get the css theme
    css_theme = nb.get('metadata', {})\
                  .get('_nbviewer', {})\
                  .get('css', None)
    if css_theme and not re.match('\w', css_theme):
        css_theme = None

    # get the notebook title
    name = nb.metadata.get('name', None)
    if not name:
        name = url.rsplit('/')[-1]
    if not name.endswith(".ipynb"):
        name = name + ".ipynb"

    # convert the body to html
    body = html_exporter.from_notebook_node(nb)[0]
    return name, css_theme, body

def request_summary(r, header=False, content=False):
    """text summary of failed request"""
    lines = [
        "%s %s: %i %s" % (
            r.request.method,
            r.url.split('?')[0],
            r.status_code,
            r.reason),
    ]
    if header:
        lines.extend([
        '--- HEADER ---',
        json.dumps(r.headers, indent=1),
        ])
    if content:
        lines.extend([
        '--- CONTENT ---',
        json.dumps(r.json(), indent=1),
        ])
    return '\n'.join(lines)





# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite://')
# app.config['GITHUB'] = {
#     'client_id': os.environ.get('GITHUB_OAUTH_KEY', ''),
#     'client_secret': os.environ.get('GITHUB_OAUTH_SECRET', ''),
# }

# import newrelic.agent
# def nrhead():
#     return newrelic.agent.get_browser_timing_header()
# def nrfoot():
#     return newrelic.agent.get_browser_timing_footer()

# @cache.cached(5*hours)
# def _hello(betauser):
#     return app.make_response(render_template('index.html', betauser=betauser))

# @app.route('/favicon.ico')
# @cache.cached(5*hours)
# def favicon():
#     return static('ico/ipynb_icon_16x16.ico')

# @app.route('/404')
# def four_o_four():
#     abort(404)

# @app.route('/400')
# def four_hundred():
#     abort(400)

# @app.route('/500')
# def five_hundred():
#     abort(500)

# @app.route('/favicon.ico')
# @cache.cached(5*hours)
# def favicon():
#     return static('ico/ipynb_icon_16x16.ico')

# @app.errorhandler(400)
# @cache.cached(5*hours)
# def page_not_found(error):
#     return render_template('400.html'), 400

# @app.errorhandler(404)
# @cache.cached(5*hours)
# def page_not_found(error):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# @cache.cached(5*hours)
# def internal_error(error):
#     return render_template('500.html'), 500

