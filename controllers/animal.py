def create():
   import datetime
   if auth.is_logged_in():
    db.animal.posted_by.default = auth.user.id
    db.animal.post_date.default = datetime.datetime.now() 
    form = crud.create(db.animal)  
    if form.process().accepted:
       response.flash = 'New advertisement created'
       redirect(URL("animal","view", args=form.vars.id))
   else:
       form = None
   return dict(form=form)

def edit():
   animal = db.animal(request.args(0, cast=int)) or redirect(URL('default','error'))
   form = crud.update("animal", animal.id, next=URL("view", args=animal.id), 
                      message="ad updated")
   return dict(animal=animal, form=form)
   

def view():
   animal = db.animal(request.args(0, cast=int)) or redirect(URL('default','error'))
   animal_author = db.auth_user(animal.posted_by)   
   if auth.is_logged_in():   
       db.comments.animal_id.default = animal.id
       db.comments.posted_by.default = auth.user.id
       db.comments.post_date.default = request.now
       form = crud.create(db.comments)	   
       if form.process().accepted:
            response.flash = 'your comment is posted'
   else:
       form = None         
   comments = db(db.comments.animal_id == animal.id).select()
   for comment in comments:
       author = db(db.auth_user.id == comment.posted_by).select()[0]
       comment.author = author.first_name + " " + author.last_name
	  
		
   return dict(animal=animal, comments=comments,form=form,  author=animal_author) 
 

