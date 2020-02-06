from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import json
import os


def get_users(req):
  try:
    # Open the file to read (assuming it exists)
    with open('users.txt', 'r') as user_files:
      user_logs = json.load(user_files)
      user_files.close()
      return user_logs
  except FileNotFoundError:
    # Create file if it does not exist
    user_files = open('users.txt', 'a+')
    user_files.close()
    return EnvironmentError


def add_users(req):
  # View the Dictionary that was Posted
  print(req)
  # Get the name (for Status just write "Status")

  newPsw = str(req.params.getall("Status"))
  newPsw = newPsw[2:len(newPsw)-2]

  newName = str(req.params.getall("name"))
  newName = newName[2:len(newName)-2]


  # Implement code to add to json()
  
  y = {"name": newName, "status": newPsw}
  try:
    with open('users.txt', 'r') as user_files:
      try:
        user_logs2 = json.load(user_files)
      except json.decoder.JSONDecodeError:
        user_files.close()
        with open('users.txt', 'w+') as user_files:
         user_logs2 = [y]
         json.dump(user_logs2, user_files)
         user_files.close()
         return user_logs2
      user_files.close()
    with open('users.txt', 'w+') as user_files:
      user_logs2.append(y)
      json.dump(user_logs2, user_files)
      return user_logs2
  except:
    return Exception













if __name__ == '__main__':
  config = Configurator()

  config.add_route('users_route', '/users')
  config.add_view(get_users, route_name='users_route', renderer='json')


  config.add_route('add_new_user', '/new_users')
  config.add_view(add_users, route_name ='add_new_user', renderer='json')



  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 5000, app)
  server.serve_forever()