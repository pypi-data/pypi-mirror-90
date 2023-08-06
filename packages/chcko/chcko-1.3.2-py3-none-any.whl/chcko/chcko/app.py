# -*- coding: utf-8 -*-

import sys
import os
from traceback import print_exc

from chcko.chcko import bottle
app = bottle.app()

from chcko.chcko.util import user_required
from chcko.chcko.hlp import chcko_import
from chcko.chcko.languages import langnumkind
from chcko.chcko.db import db
from functools import partial

def no_null_requests(end_of_route):
    if end_of_route is None:
        return
    if end_of_route.endswith('null'): #XXX: why does this null happen?
        raise bottle.HTTPError(404,'404_1')

def lang_pagename(lang=None,pagename=None):
    if lang is None:
        lang = db.get_cookie('chcko_cookie_lang')
    if lang not in langnumkind:
        if pagename == None:
            pagename = lang
        langs = bottle.request.headers.get('Accept-Language')
        if langs:
            langs = langs.split(',')
        else:
            langs = ['en-US', 'en;q=0.8', 'de']
        accepted = set([x.split(';q=')[0].split('-')[0] for x in langs])
        candidates = accepted & db.available_langs
        if candidates:
            if 'en' in candidates:
                lang = 'en'
            else:
                lang = list(candidates)[0]
        else:
            lang = 'en'
    if pagename is None:
        pagename = 'contents'
    return lang,pagename

@bottle.hook('before_request')
def normalize_url():
    orgpath = bottle.request.environ['PATH_INFO']
    bottle.request.environ['PATH_INFO'] = orgpath.rstrip('/')

pj = os.path.join

#not installed parallel chcko-xyz plus chcko
ROOTS = [x for x in sys.path
         if x.endswith('site-packages') or os.path.split(x)[1].startswith('chcko')]
d = os.path.dirname
ROOT = d(d(d(__file__)))
def findstatic(filename):
    res = bottle.HTTPError(404,'404_A '+filename)
    for r in ROOTS:
        res = bottle.static_file(filename,root=r)
        if not isinstance(res,bottle.HTTPError):
            return res
    return res

# for google verification
# test: http://localhost:8080/google509fdbaf2f77476f.html
@bottle.route('/<filename>.html')
def statichtml(filename):
    if len(filename.split(os.sep)) > 1:
        return bottle.HTTPError(403,'403_2')
    if not os.path.splitext(filename)[1]:
        filename = filename+'.html'
    return findstatic(pj('chcko',filename))

# test: http://localhost:8080/favicon
@bottle.route('/favicon.ico')
def serve_favicon():
    return bottle.static_file(pj('chcko','chcko','static','favicon.ico'),root=ROOT)

# test:
# http://localhost:8080/en/_images/r_dg_c1.png
# http://localhost:8080/_images/r_dg_c1.png
# http://localhost:8080/r_dg_c1.png
@bottle.route('/<chlang>/_images/<filename>')
@bottle.route('/_images/<filename>')
@bottle.route('/<filename>.png')
def serve_image(filename,chlang='en'):
    no_null_requests(filename)
    if len(filename.split(os.sep)) > 1:
        return bottle.HTTPError(403,'403_3')
    if not os.path.splitext(filename)[1]:
        filename = filename+'.png'
    return findstatic(pj('chcko','_images',filename))

# test:
# http://localhost:8080/static/main.css
@bottle.route('/static/<filename>')
def serve_static(filename):
    no_null_requests(filename)
    if len(filename.split(os.sep)) > 1:
        return bottle.HTTPError(403,'403_4')
    return findstatic(pj('chcko','chcko','static',filename))

#social
try:
    from social_core.exceptions import SocialAuthBaseException
    from social_core.actions import do_auth, do_complete
    from chcko.chcko.auth import make_backend_obj, social_login_name
    @bottle.route('/auth/<provider>', method=('GET', 'POST'))
    @make_backend_obj()
    def auth_login(backend):
        try:
            backend.strategy.session_pop(backend.name + '_state')
            do_auth(backend)
        except SocialAuthBaseException:
            bottle.redirect('/')
    @bottle.route('/auth/<provider>/callback', method=('GET', 'POST'))
    @make_backend_obj()
    def auth_callback(backend):
        try:
            user = do_complete(backend, login=None)
        except SocialAuthBaseException:
            pass
        db.set_cookie('chcko_cookie_usertoken',bottle.request.user.token)
        bottle.redirect('/')
    #this is called via social_core
    def social_user(backend, uid, user=None, *args, **kwargs):
        sln = social_login_name(backend.__class__)
        info = kwargs['details']
        fullname = f'{info["fullname"]} ({sln})'
        jwt = kwargs['response']
        try:
            chlang = jwt['locale']
        except:
            chlang = 'en'
        email = info['email']
        verified = True
        if not email:
            email = fullname
            verified = False
        token = db.token_create(email)
        user, token = db.user_login(email,fullname=fullname,token=token,chlang=chlang,verified=verified)
        bottle.request.user = user
        #statisfy social_core:
        class AttributeDict(dict): 
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        kwargs['user'] = AttributeDict()
        kwargs['social'] = user
        kwargs['is_new'] = None
        kwargs['user'].social = user
        return kwargs
except:
    pass

@bottle.route('/',method=['GET','POST'])
def nopath():
    return fullpath(None,None)

@bottle.route('/<chlang>',method=['GET','POST'])
def langonly(chlang):
    no_null_requests(chlang)
    return fullpath(chlang,None)

@bottle.route('/<chlang>/logout')
def logout(chlang):
    t = db.get_cookie('chcko_cookie_usertoken')
    if t:
        db.token_delete(t)
        bottle.response.delete_cookie('chcko_cookie_usertoken')
    bottle.redirect(f'/{chlang}/contents')

@bottle.route('/<chlang>/<pagename>',method=['GET','POST'])
def fullpath(chlang,pagename,**kextra):
    no_null_requests(pagename)
    try:
        chlang,pagename = lang_pagename(chlang,pagename)
    except ValueError:
        return ""
    db.set_cookie('chcko_cookie_lang',chlang)
    bottle.request.chlang = chlang
    bottle.request.pagename = pagename
    db.user_by_cookie()
    db.student_by()
    try:
        mod = chcko_import('chcko.'+pagename)
        page = mod.Page(mod)
        if bottle.request.route.method == 'GET':
            respns = page.get_response(**(kextra if kextra else bottle.request.params))
        else:
            respns = page.post_response()
        return respns
    except (ImportError, AttributeError, IOError, NameError) as e:
        print_exc()
        bottle.redirect(f'/{chlang}')
    except bottle.HTTPError:
        raise
    except bottle.HTTPResponse:
        raise
    except:
        print_exc()
        pagename = "message"
        bottle.request.pagename = pagename
        mod = chcko_import('chcko.'+pagename)
        page = mod.Page(mod)
        respns = page.get_response()
        return respns

@bottle.error(400)
@bottle.error(403)
@bottle.error(404)
def no_permission(error):
    try:
        return fullpath(None,'message',msg='',errormsg=error.body)
    except:
        mod = chcko_import('chcko.message')
        page = mod.Page(mod)
        return page.get_response(msg='',errormsg=error.body)

