from flask import Flask, render_template, request, url_for
import os
from flask import flash,redirect
from werkzeug.utils import secure_filename
import os
import shutil
from PIL import Image
from tensorflow import keras
from keras.layers import Dense
from keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
import numpy as np

def predict_model(img):
    model =  load_model('weathermodel.h5')
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis = 0)
    preds = model.predict(x)
    pred = np.argmax(preds,axis = 1)
    index = ['cloudy','foggy','rainy','sunshine','sunrise']
    result = str(index[pred[0]])
    return(result)

def resize_image(image_path, width, height):

    with Image.open(image_path) as img:
        resized_img = img.resize((width, height))
        resized_img.save(image_path)
        
app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
@app.route('/about.html')
def about():
    return render_template('about.html')    
@app.route('/pictures.html')
def pictures():
    return render_template('pictures.html')
@app.route('/upload.html')
def up():
    return render_template('upload.html') 
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    print(filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    path = 'static/{}'.format(filename)
    resize_image(path,300,300)
    img = image.load_img(path,target_size = (180,180))
    result = predict_model(img)
    return render_template('res.html', image_url=url_for('static', filename=filename),result = result)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'static'
    app.run(debug=True)



