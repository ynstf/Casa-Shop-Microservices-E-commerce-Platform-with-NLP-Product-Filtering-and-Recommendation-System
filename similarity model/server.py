import pandas as pd
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, jsonify

from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
version = 1
model_folder = f"model_v{version}"
max_length = 32
siamese_lstm_model = load_model(f'{model_folder}/model.h5')

app = Flask(__name__)

class InputData:
    def __init__(self, data):
        self.data = data

@app.route("/")
def welcome():
    return "Welcome"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get('data')  # Extract data from the request
    print(data)
    input_data = InputData(data)  # Create InputData object

    version = 1
    model_folder = f"model_v{version}"
    max_length = 32

    # Load the tokenizer configuration from the JSON file
    with open(f'{model_folder}/tokenizer_config.json', 'r') as json_file:
        tokenizer_config_json = json_file.read()

    # Recreate the tokenizer object
    tokenizer = tokenizer_from_json(tokenizer_config_json)

    # Load the model
    siamese_lstm_model = load_model(f'{model_folder}/model.h5')

    df = pd.read_csv(f'{model_folder}/data.txt')
    df = df.drop_duplicates(subset='Name of Product', keep='first')

    index = df.index[df["Name of Product"] == input_data.data].tolist()[0]
    df["name"] = df["Name of Product"][index]

    # Prepare test data
    X_test_text1 = pad_sequences(tokenizer.texts_to_sequences(df['name']), maxlen=max_length)
    X_test_text2 = pad_sequences(tokenizer.texts_to_sequences(df['Name of Product']), maxlen=max_length)
    simi = siamese_lstm_model.predict([X_test_text1, X_test_text2])

    df["similarity"] = simi

    # Convert relevant data to JSON serializable format
    result = {
        "data": input_data.data,
        "precision": list(df[df["similarity"]>0.85]["Name of Product"])
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

