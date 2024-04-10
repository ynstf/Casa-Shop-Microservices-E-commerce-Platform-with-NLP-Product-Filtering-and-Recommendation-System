from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
version = 1
model_folder = f"model_v{version}"
max_length = 32
siamese_lstm_model = load_model(f'{model_folder}/model.h5')
