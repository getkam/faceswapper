from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session
import os
import cv2
from jinja2 import Environment
import helper
from helper import login_required
import sqlite3
import re
import bcrypt

import insightface 
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
app.secret_key = "super secret key"
Session(app)

env = Environment()
app.jinja_env.globals.update(enumerate=enumerate)

face_analysis = FaceAnalysis(name='buffalo_l')
face_analysis.prepare(ctx_id=0, det_size=(640,640))


@app.route('/')
def index():
    if "user_id" in session: 
        return render_template('index.html')
    else:
        return redirect('/welcome')
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        # Ensure username was submitted
        if not username:
            return render_template("login.html", error="User name must be provided")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="Password must be provided")
        
        with sqlite3.connect('faceswapper.db') as conn:
            # Set row_factory na sqlite3.Row
            conn.row_factory = sqlite3.Row  
            db = conn.cursor()
            # Query database for username
            row = db.execute("SELECT id, hash FROM users WHERE username = ?", [username]).fetchone()
            # Ensure username exists and password is correct
            if row is None:
                return render_template("login.html", error="Invalid username. Please try again.")
            provided_password = request.form.get("password").encode('utf-8')
            hashed_password = row["hash"]
            if not bcrypt.checkpw(provided_password, hashed_password):
                return render_template("login.html", error="Invalid password. Please try again.")

            # Remember which user has logged in
            session["user_id"] = row["id"]
            session.permanent = True
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""
    if request.method == "POST":
      with sqlite3.connect('faceswapper.db') as conn:
        db = conn.cursor()
        username = request.form.get("username")
        print(username)
        if not username:
            return render_template("signup.html", error="Username must be provided")
        userDB = db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()
        if len(userDB) != 0:
            return render_template("signup.html", error="Username already exists")

        password = request.form.get("password")
        if len(password) < 5 or not re.search(r"[a-z]", password) or not re.search(r"[\d]", password):
            return render_template("signup.html", error="Password must be at least 5 characters long and contain at least one number and one letter")

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return render_template("signup.html", error="Passwords do not match")
        password_bytes = password.encode('utf-8')
        print(password_bytes)
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        print(hashed)
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", (username,hashed)
        )
        return redirect("/")
    if request.method == "GET":
        return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    clear()
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return render_template("login.html", error="You have been successfully log out. All your data has been removed")


@app.route('/upload', methods=['POST'])
@login_required
def upload():
  if request.method == "POST":

    # Recognize which picture is being uploaded
    if 'target' in request.files or 'source' in request.files or 'biometric' in request.files:
      if 'target' in request.files:
          type = 'target'
      elif 'source' in request.files:
          type = 'source'
      elif 'biometric' in request.files:
          type = 'biometric'

      # Check if the file is an image 
      if not helper.isImage(request.files[type].filename):
        if type == 'biometric':
            return render_template('biometric.html',error="Please upload an image file")
        return render_template('index.html',error="Please upload an image file")
      
      # Save the file
      file = request.files[type]
      file_path = os.path.join('./static/images/', file.filename)
      os.makedirs(os.path.dirname(file_path), exist_ok=True)
      file.save(file_path)

      # Save the file path in the session
      session[type+'_img'] = file_path

      # Read saved file and detect faces
      img = cv2.imread(file_path)
      faces = face_analysis.get(img)
      
      # Check if any faces were detected
      if len(faces) == 0:
        if type == 'biometric':
            return render_template('biometric.html',error="No faces detected in the image")
        return render_template('index.html',error="No faces detected in the image")
      
      # Organize recognized faces in a list
      recognized_faces = []
      for i, face in enumerate(faces):
          bbox = face['bbox']
          bbox = [int(b) for b in bbox]
          face_image = img[bbox[1]:bbox[3], bbox[0]:bbox[2],::1]

          # Save recognized face image in the static folder
          cv2.imwrite(f'./static/images/{type}_face_{i}.jpg', face_image)

          # Add the path to the recognized_faces list
          recognized_faces.append(f'./static/images/{type}_face_{i}.jpg')

      # Save the recognized faces in the session
      session[type+'_faces'] = recognized_faces

      # no need to pass pictures, everything is in the session
      if type == 'biometric': 
          return redirect('/biometric')
      return render_template('index.html')
    else:
        if type == 'biometric': 
          return render_template('biometric.html', error="Please upload an image file")
        return render_template('index.html', error="Please upload an image file")
  else:
      if type == 'biometric': 
          return redirect('/biometric')
      return render_template('index.html')


@app.route('/swap', methods=['POST'])
@login_required
def swap():
   if request.method == "POST":
      if 'target_img' in session and 'source_img' in session:
         # Use the model to swap the faces
         swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)

         # Load the images
         original_target = cv2.imread(session.get('target_img'))
         original_source = cv2.imread(session.get('source_img'))

         # Recognize the faces in the images
         target_faces = face_analysis.get(original_target)
         source_faces = face_analysis.get(original_source)

         # Copy the target image to avoid modifying the original
         copy_img = original_target.copy()
         
         # Get the selected faces
         target_idx = int(request.form.get('selected_target_face'))
         source_idx = int(request.form.get('selected_source_face'))

         # Swap the faces
         copy_img = swapper.get(copy_img, target_faces[target_idx], source_faces[source_idx], paste_back=True)

         # Save the result
         cv2.imwrite(f'./static/images/result.jpg', copy_img)
         session['result_img'] = './static/images/result.jpg'

         # Render the result page
         return render_template('result.html')
      else:
        return render_template('index.html', error="Please upload an image file")
   else:
      return render_template('index.html')
   
@app.route('/biodata', methods=['POST'])
@login_required
def biodata():
   if request.method == "POST":
      if 'biometric_img' in session:
         # Use the model to swap the faces
         swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)

         # Load the images
         original_file= cv2.imread(session.get('biometric_img'))
         

         # Recognize the faces in the images
         faces = face_analysis.get(original_file)
         
         selected_face_idx=int(request.form.get('selected_biometric_face'))
        
         session["selected_bio_face_idx"]=selected_face_idx
         age = faces[selected_face_idx]['age']
         
         # Render the result page
         return render_template('biometric.html', age = age )
      else:
        return render_template('biometric.html', error="Please upload an image file")
   else:
      return render_template('biometric.html')
     

@app.route('/clear', methods=['POST'])
@login_required
def clear():
    # Clear the session and remove the files
    if 'target_img' in session:
        os.remove(session.get('target_img'))
    if 'source_img' in session:
        os.remove(session.get('source_img'))
    if 'biometric_img' in session:
        os.remove(session.get('biometric_img'))
    if 'target_faces' in session:
        for face in session.get('target_faces'):
            os.remove(face)
    if 'source_faces' in session:
        for face in session.get('source_faces'):
            os.remove(face)
    if 'biometric_faces' in session:
        for face in session.get('biometric_faces'):
            os.remove(face)
    if 'result_img' in session:
        os.remove(session.get('result_img'))
    
    userid = session.get("user_id")
    session.clear()
    session["user_id"]=userid

    return render_template('index.html', error="All uploaded files has been deleted")

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/biometric',methods=["GET", "POST"])
@login_required
def biometric():
    return render_template('biometric.html')
