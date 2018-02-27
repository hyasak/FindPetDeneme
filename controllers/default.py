# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    animals_last=db().select(db.animal.ALL, orderby=~db.animal.id, limitby=(0,3))
    return dict(animals=animals_last)

def data(): 
    return dict(form=crud())

def profile():
    username  = request.args(0) or redirect(URL('default','error'))
    rows = db(db.auth_user.username == username).select()
    if len(rows) > 0:
       user = rows[0]
    else:
       user = None   
    return dict(user=user)
	
def animals():		
    animals=db().select(db.animal.ALL, orderby=db.animal.id)
    return dict(animals=animals )

def city():
	city = db.cities(request.args(0, cast=int)) or redirect(URL('default','error')) 
	animals=db().select(db.animal.ALL, orderby=db.animal.id)
	animal_in_city=db(db.animal.city == city).select()
	return dict(animals=animal_in_city)
	
def cities():
   animal_cities=db().select(db.animal.city, orderby=db.animal.city, distinct=True )
   return dict(cities=animal_cities)


	
def about():

    return dict()

def contact():
    return dict()

def report():
	return dict()
	
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('editor')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
def error():
	return dict()