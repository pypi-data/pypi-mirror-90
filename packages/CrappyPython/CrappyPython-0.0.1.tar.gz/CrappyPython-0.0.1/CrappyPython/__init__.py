import random
import datetime
import Urls34 as urls
import os as aw

def rc(a):
  return random.choice(a)

def ri(a:int,b:int):
  return random.randint(a,b)

def ct():
  return datetime.datetime.now()

def response(url):
  return urls.get_response(url)

def rnd(a:float):
  return round(a)

def install(module_name):
  aw.system("pip install "+module_name)

def cl():
  aw.system("clear")

def urlcontext(url,file=None,file_name="Url"):
  if file==None:
    return urls.urlread(url)
  if file==True:
    rl=urls.urlread(url)
    f=open(file_name,"w+")
    f.write(str(rl))
    f.close()
def credits():
  return "Modules used: random, datetime, Urls34, os. Module links(in order): Not Found, Too Many Results, https://pypi.org/project/Urls34/, https://pypi.org/search/?q=os"

def CrappyPython(ctx):
  return eval(ctx)