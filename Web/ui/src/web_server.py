from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response

import requests
import os

REST_SERVER = os.environ['REST_SERVER']


#Show all the users in the database
def show_users(req):
  # "/users" comes from the route defined in rest_server.py
  Users = requests.get(REST_SERVER + "/users").json()
  # The word "users" is a variable that is used in the show_users.html
  return render_to_response('templates/show_users.html', {'users': Users}, request=req)



def add_new_user(req):
  print("||||||||||||||||-->>>>> ")
  # GEt all the data that is going to be sent (needs to be a dict like "data")
  print(req.GET)
  data = {"name": "Apple-Boy", "Status": "fuck you server"}
  New_user = requests.post(REST_SERVER + '/new_user', data = data).json()
  print("||||||||||||||||   List of users in table:", end ='')
  print(New_user)
  return render_to_response('templates/show_users.html', {'users': New_user}, request=req)





# Compare credentials from request to json
def valid_user(req):
  #-------------code to make ---------------#
  return False


# Route to validate login credentials...
def post_login(req):
  if valid_user(req):
    return render_to_response('templates/did_log_in.html', {}, request = req)
  else:
    return render_to_response('templates/show_log.html', {'error': 'invalid user'}, request=req)

# These currently just render the html files 
def sign_up(req):
  return render_to_response('templates/sign_up.html', {}, request =req)

def portal(req):
  return render_to_response('templates/portal.html', {}, request =req)

def login(req):
  return render_to_response('templates/did_log_in.html', {}, request =req)


########################################################################################
#                           Main Function
########################################################################################
if __name__ == '__main__':

  config = Configurator()
  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  # This is the main page localhost:50000
  # Adds a route v2 so you can have localhost:5000/ or localhost:5000/v2
  config.add_route('v2', '/')
  # Loading stuff from the server
  config.add_view(portal, route_name='v2')
  

  config.add_route('show_users', '/show_users')
  config.add_view(show_users, route_name='show_users')


  config.add_route('new_user', '/new_user')
  config.add_view(show_users, route_name='new_user')
  config.add_view(add_new_user, route_name='new_user', request_method = "POST")

  config.add_route('sign_up', '/sign_up')
  config.add_view(sign_up, route_name='sign_up')
  

  config.add_route('login', '/login')
  config.add_view(login, route_name='login')



  config.add_static_view(name='/', path = './public', cache_max_age = 3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()
