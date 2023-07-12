import os
import uuid
import flask
import urllib  
import tensorflow  as tf
import numpy as np
from PIL import Image
from tensorflow import keras
from keras.models import load_model
from flask import Flask , render_template , request
from keras.utils import load_img
from tensorflow import _keras


app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'finalmodel.h5'))


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif', 'JPG'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

classes = [
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites_Two_spotted_spider_mite',
 'Tomato__Target_Spot',
 'Tomato__Tomato_YellowLeaf__Curl_Virus',
 'Tomato__Tomato_mosaic_virus',
 'Tomato_healthy']


def predict(filename , model):
    img = load_img(filename , target_size = (256 , 256))

    img  = np.array(img)
    img_array = np.expand_dims(img,0)
    result = model.predict(img_array)
    

    dict_result = {}
    for i in range(10):
        dict_result[result[0][i]] = classes[i]

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]
    
    prob_result = []
    class_result = []
    for i in range(3):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])

    return class_result , prob_result




@app.route('/')
def home():
        return render_template("index.html")


@app.route('/bacterialspot', methods=['GET'])
def disease1():
     return render_template('bacterial-leaf.html')


@app.route('/earlyblight', methods=['GET'])
def disease2():
     return render_template('early_blight.html')


@app.route('/healthyleaf', methods=['GET'])
def disease3():
     return render_template('healthy_leaf.html')


@app.route('/lateblight', methods=['GET'])
def disease4():
     return render_template('late_blight.html')


@app.route('/leafmold', methods=['GET'])
def disease5():
     return render_template('leaf_mold.html')


@app.route('/mosaicvirus', methods=['GET'])
def disease6():
     return render_template('mosaic_virus.html')


@app.route('/septorialleaf', methods=['GET'])
def disease7():
     return render_template('septorial_leaf.html')


@app.route('/spidermite', methods=['GET'])
def disease8():
     return render_template('spider_mite.html')


@app.route('/targetspot', methods=['GET'])
def disease9():
     return render_template('target_spot.html')


@app.route('/yellowleaf', methods=['GET'])
def disease10():
     return render_template('yellow_leaf.html')


@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static')
    if (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                class_result , prob_result = predict(img_path , model)

                predictions = {
                      "class1":class_result[0],
                        "class2":class_result[1],
                        "class3":class_result[2],
                        "prob1": prob_result[0],
                        "prob2": prob_result[1],
                        "prob3": prob_result[2],
                }

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('index.html' , error = error)

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True)
