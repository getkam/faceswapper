from functools import wraps
from flask import Flask, redirect, session

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if session.get("user_id") is None:
      return redirect("/login")
    return f(*args, **kwargs)
  return decorated_function

def isImage(file):
  length = len(file.rsplit('.'))
  return ('.' in file and file.rsplit('.')[length - 1].lower() in ['png', 'jpg', 'jpeg'])
