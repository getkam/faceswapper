from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session, sessions
import numpy as np
import os
import glob
import cv2
import matplotlib.pyplot as plt
from jinja2 import Environment
import helper

import insightface 
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)
app.secret_key = "super secret key"
Session(app)

env = Environment()
app.jinja_env.globals.update(enumerate=enumerate)

face_analysis = FaceAnalysis(name='buffalo_l')
face_analysis.prepare(ctx_id=0, det_size=(640,640))

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
  if request.method == "POST":

    # Recognize which picture is being uploaded
    if 'target' in request.files or 'source' in request.files:
      if 'target' in request.files:
          type = 'target'
      elif 'source' in request.files:
          type = 'source'

      # Check if the file is an image 
      if not helper.isImage(request.files[type].filename):
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
      return render_template('index.html')
    else:
        return render_template('index.html', error="Please upload an image file")
  else:
      return render_template('index.html')


@app.route('/swap', methods=['POST'])
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
   

@app.route('/clear', methods=['POST'])
def clear():
    # Clear the session and remove the files
    if 'target_img' in session:
        os.remove(session.get('target_img'))
    if 'source_img' in session:
        os.remove(session.get('source_img'))
    if 'target_faces' in session:
        for face in session.get('target_faces'):
            os.remove(face)
    if 'source_faces' in session:
        for face in session.get('source_faces'):
            os.remove(face)
    if 'result_img' in session:
        os.remove(session.get('result_img'))
    
    session.clear()
    return render_template('index.html')
