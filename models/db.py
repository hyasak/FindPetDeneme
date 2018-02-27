# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
animal_kinds = "Dog Cat Reptile Bird Other".split()
vaccine_types="Yes No".split()
genders="Female Male".split()

db.define_table('cities',
				Field('name'),
				format = '%(name)s'
				)

auth.settings.extra_fields['auth_user']= [               
				Field('image','upload'),
				Field('bio'),
                Field('gender', 'list:string'),
                Field('age', 'integer'),
                Field('city', 'reference cities') 
				]
auth.define_tables(username=True, signature=False)

db.auth_user.username.requires =[IS_NOT_EMPTY(error_message = 'This field can not be empty!'),
                           IS_NOT_IN_DB(db, 'auth_user.username', error_message='Invalid username')]
db.auth_user.city.requires = IS_NOT_EMPTY(error_message = 'Please enter a city!')
db.auth_user.bio.requires = IS_NOT_EMPTY(error_message = 'Your biography is required for the profile!')
db.auth_user.age.requires = requires = IS_INT_IN_RANGE(16, 120, error_message='You should be at least 16 to register!')
db.auth_user.gender.requires = IS_IN_SET(genders)
db.auth_user.image.requires = IS_EMPTY_OR(IS_IMAGE(extensions=('jpeg', 'png')))

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)





				
db.define_table('animal',
                 Field('name', unique=True),  
				 Field('kind', 'list:string'),
				 Field('vaccine','list:string'),
				 Field('city', 'reference cities'),
				 Field('gender','list:string'),
				 Field('age','integer'),
				 Field('image','upload'),
				 Field('description'),
                 Field('posted_by', 'reference auth_user'),
				 Field('post_date', 'datetime'),                 
                 format = '%(name)s'
               )

db.define_table('comments',
                Field('body', 'text'),                
                Field('posted_by', 'reference auth_user'),
				Field('animal_id', 'reference animal'),
                Field('post_date', 'datetime'),                
                format = '%(posted_by)s comment on %(animal_id)s'
              )
			  

db.animal.city.requires = IS_NOT_EMPTY(error_message = "You need to enter the city!")
db.animal.image.requires = IS_IMAGE(error_message = 'Please upload a photo of our friend :)!')
db.animal.description.requires = IS_NOT_EMPTY(error_message = 'Please give some info!')
                            
db.animal.kind.requires=IS_IN_SET(animal_kinds) 
db.animal.vaccine.requires=IS_IN_SET(vaccine_types)
db.animal.gender.requires=IS_IN_SET(genders)


db.auth_user.city.requires=IS_IN_DB(db, db.cities.id, error_message="You need to select the city!")					   
db.animal.city.requires=IS_IN_DB(db, db.cities.id, error_message="You need to select the city!")

db.comments.body.requires = IS_NOT_EMPTY(error_message = "You cannot post empty comment!")
db.comments.animal_id.requires = IS_IN_DB(db, db.animal.id)
db.animal.posted_by.requires = IS_IN_DB(db, db.auth_user.id)               
db.comments.posted_by.requires = IS_IN_DB(db, db.auth_user.id)


db.animal.posted_by.writable = db.animal.posted_by.readable = False
db.animal.post_date.writable = db.animal.post_date.readable = False
db.comments.animal_id.writable = db.comments.animal_id.readable = False
db.comments.post_date.writable = db.comments.post_date.readable = False
db.comments.posted_by.writable = db.comments.posted_by.readable = False

from gluon.tools import Crud
crud = Crud(db)



