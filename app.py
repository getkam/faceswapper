from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session, sessions
import numpy as np
import os
import glob
import cv2
import matplotlib.pyplot as plt
from jinja2 import Environment

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
    if 'target' in request.files or 'source' in request.files:
      if 'target' in request.files:
          type = 'target'
      elif 'source' in request.files:
          type = 'source'
      file = request.files[type]
      file_path = os.path.join('./static/images/', file.filename)
      os.makedirs(os.path.dirname(file_path), exist_ok=True)
      file.save(file_path)
      session[type+'_img'] = file_path
      
      img = cv2.imread(file_path)
      faces = face_analysis.get(img)
      recognized_faces = []

      for i, face in enumerate(faces):
          bbox = face['bbox']
          bbox = [int(b) for b in bbox]
          face_image = img[bbox[1]:bbox[3], bbox[0]:bbox[2],::1]
          cv2.imwrite(f'./static/images/{type}_face_{i}.jpg', face_image)
          recognized_faces.append(f'./static/images/{type}_face_{i}.jpg')

      session[type+'_faces'] = recognized_faces

      return render_template('index.html', target_img=session.get('target_img'), source_img=session.get('source_img'), target_faces=session.get('target_faces'), source_faces=session.get('source_faces'))

    else:
        return render_template('index.html')
  else:
      return render_template('index.html')


@app.route('/swap', methods=['POST'])
def swap():
   if request.method == "POST":
      if 'target_img' in session and 'source_img' in session:
         swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False);
         original_target = cv2.imread(session.get('target_img'))
         original_source = cv2.imread(session.get('source_img'))
         target_faces = face_analysis.get(original_target)
         source_faces = face_analysis.get(original_source)
         copy_img = original_target.copy()
         
         target_idx = int(request.form.get('target_face'))

         source_idx = int(request.form.get('source_face'))

         copy_img = swapper.get(copy_img, target_faces[target_idx], source_faces[source_idx], paste_back=True)
         cv2.imwrite(f'./static/images/result.jpg', copy_img)
         return render_template('result.html', result_img='./static/images/result.jpg')
      else:
        return render_template('index.html')
   else:
      return render_template('index.html')
