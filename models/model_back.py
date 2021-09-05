from tensorflow.keras import Model
from tensorflow.keras.layers import *

# baseline neural network
class PredictionNet(Model):
    def __init__(self, features_shape, name = None):
        super(PredictionNet, self).__init__(name=name)
        self.first_layer = Dense(features_shape*8, activation = 'relu')
        self.second_layer = Dense(features_shape*4, activation = 'relu')
        self.third_layer = Dense(features_shape*4, activation = 'relu')
        self.final = Dense(1)
    def call(self, x):
        x = self.first_layer(x)
        x = self.second_layer(x)
        x = self.third_layer(x)
        return self.final(x)