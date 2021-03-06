from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

import requests
import os

REST_SERVER = os.environ['REST_SERVER']


# Show all the users in the database
def show_users(req):
  # "/users" comes from the route defined in rest_server.py
  Users = requests.get(REST_SERVER + "/users").json()
  # The word "users" is a variable that is used in the show_users.html
  return render_to_response('templates/show_users.html', {'users': Users}, request=req)



def add_new_user(req):
  # Get all the data that is going to be sent (needs to be a dict like "data")
  # print(req.params) #debugging
  data = {"Username": req.params['Username'], "Password":  req.params['Password']}
  New_user = requests.post(REST_SERVER + '/new_users', data = data).json()
  return render_to_response('templates/portal.html', {}, request=req)

def changestatus(req):
  # Get all the data that is going to be sent (needs to be a dict like "data")
  print("---------------------------------->")
  print(req.params["Status"]) #debugging
  print("---------------------------------->")
  data = {"Username" : req.params['Username'], "Status": req.params['Status']}
  newstatus = requests.post(REST_SERVER + '/change_status', data = data).json()
  return render_to_response('templates/adminportal.html', {'Users': newstatus}, request=req)

# Compare credentials from request (from user) to json
def valid_user(req):
  data = {"Username": req.params['Username'], "Password":  req.params['Password']}
  validity = requests.post(REST_SERVER + '/check_valid', data = data).json()
  return validity


# Route to validate login credentials...
def post_login(req):
  if valid_user(req):
    return admin(req)
  else:
    return render_to_response('templates/did_log_in.html', {'tag': 'Incorrect Password'}, request = req)

# These currently just render the html files 
def sign_up(req):
  return render_to_response('templates/sign_up.html', {}, request =req)

def portal(req):
  return render_to_response('templates/portal.html', {}, request =req)
 
def login(req):
  return render_to_response('templates/did_log_in.html', {}, request =req)

def admin(req):
  Users = requests.get(REST_SERVER + "/users").json()
  return render_to_response('templates/adminportal.html',{'users': Users}, request =req)



########################################################################################
#                      Stupidest some people take     Main Function
########################################################################################
if __name__ == '__main__':

  config = Configurator()
  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  # This is the "MAIN" page localhost:50000
  # Adds a route v2 so you can have localhost:5000/ or localhost:5000/v2
  config.add_route('v2', '/')
  # Loading stuff from the server
  config.add_view(portal, route_name='v2')
  

  config.add_route('show_users', '/show_users')
  config.add_view(show_users, route_name='show_users')  
  
  config.add_route('admin', '/admin')
  config.add_view(admin, route_name='admin')

  config.add_route('changestatus', '/changestatus')
  config.add_view(changestatus, route_name='changestatus', request_method = "POST")


  config.add_route('new_user', '/new_user')
  config.add_view(show_users, route_name='new_user')
  config.add_view(add_new_user, route_name='new_user', request_method = "POST")

  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up')
  

  config.add_route('login', '/login')
  config.add_view(login, route_name='login')
 
  config.add_route('post_login', '/post_login')
  config.add_view(post_login, route_name='post_login', request_method = "POST")


  config.add_static_view(name='/', path = './public', cache_max_age = 3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()
