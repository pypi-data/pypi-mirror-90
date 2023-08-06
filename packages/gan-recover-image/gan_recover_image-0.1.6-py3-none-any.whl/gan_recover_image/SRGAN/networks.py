import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Flatten, Dense, Input, Conv2D, BatchNormalization, LeakyReLU, PReLU, Add, \
    UpSampling2D, Activation
from tensorflow.keras.models import Model
from PIL import Image
import os


class UpSampleBlock(Model):
    def __init__(self, input_shape, kernel_size, filters, strides):
        super().__init__()
        assert (filters > 0 and kernel_size > 0 and strides > 0), "Input arguments are positive!"
        input_layer = Input(shape=input_shape)
        model = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(input_layer)
        model = UpSampling2D(size=2)(model)
        model = PReLU(alpha_initializer="zeros", alpha_regularizer=None, alpha_constraint=None, shared_axes=[1, 2])(
            model)
        self.model = Model(input_layer, model)

    def __call__(self, input, training=None):
        return self.model(input, training=training)

    def summary(self):
        return self.model.summary()


def UpSampleBlock(model, kernel_size, filters, strides):
    model = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(model)
    model = UpSampling2D(size=2)(model)
    model = PReLU(alpha_initializer="zeros", alpha_regularizer=None, alpha_constraint=None, shared_axes=[1, 2])(model)
    return model


class DiscBlock(Model):
    def __init__(self, input_shape, kernel_size, filters, strides):
        super().__init__()
        assert (filters > 0 and kernel_size > 0 and strides > 0), "Input arguments are positive!"
        input_layer = Input(shape=input_shape)
        model = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(input_layer)
        model = BatchNormalization()(model)
        model = LeakyReLU(alpha=0.2)(model)
        self.model = Model(input_layer, model)

    def __call__(self, input, training=None):
        return self.model(input, training=training)

    def summary(self):
        return self.model.summary()


def DiscBlock(model, filters, kernel_size, strides):
    model = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(model)
    model = BatchNormalization()(model)
    model = LeakyReLU(alpha=0.2)(model)
    return model


class ResBlock(Model):
    def __init__(self, input_shape, kernel_size, filters, strides):
        super().__init__()
        assert (filters > 0 and kernel_size > 0 and strides > 0), "Input arguments are positive!"
        input_layer = Input(shape=input_shape)
        model = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(input_layer)
        model = BatchNormalization()(model)
        # model = LeakyReLU(alpha=0.2)(model)
        model = PReLU(alpha_initializer="zeros", alpha_regularizer=None, alpha_constraint=None, shared_axes=[1, 2])(
            model)
        model = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(model)
        model = BatchNormalization()(model)
        model = Add()([input_layer, model])

        self.model = Model(input_layer, model)

    def __call__(self, input, training=None):
        return self.model(input, training=training)

    def summary(self):
        return self.model.summary()


def ResBlock(model, kernel_size, filters, strides):
    x = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(model)
    x = BatchNormalization()(x)
    x = PReLU(alpha_initializer="zeros", alpha_regularizer=None, alpha_constraint=None, shared_axes=[1, 2])(x)
    x = Conv2D(filters=filters, kernel_size=kernel_size, strides=strides, padding="same")(x)
    x = BatchNormalization()(x)
    x = Add()([model, x])
    return x


class Generator(Model):
    def __init__(self, input_shape):
        super().__init__()

        gen_input = Input(shape=input_shape)

        model = Conv2D(filters=64, kernel_size=9, strides=1, padding="same")(gen_input)
        model = PReLU(alpha_initializer='zeros', alpha_regularizer=None, alpha_constraint=None, shared_axes=[1, 2])(
            model)
        gen_model = model

        # Using 16 Residual Blocks
        for index in range(16):
            model = ResBlock(model, 3, 64, 1)

        model = Conv2D(filters=64, kernel_size=3, strides=1, padding="same")(model)
        model = BatchNormalization()(model)
        model = Add()([gen_model, model])

        # Using 2 UpSampling Blocks
        for index in range(2):
            model = UpSampleBlock(model, 3, 256, 1)

        model = Conv2D(filters=3, kernel_size=9, strides=1, padding="same")(model)
        model = Activation('tanh')(model)

        self.model = Model(inputs=gen_input, outputs=model)

    def __call__(self, input, training=None):
        return self.model(input, training=training)

    def summary(self):
        return self.model.summary()

    def load_weights(self, latest_ckpt):
        return self.model.load_weights(latest_ckpt)

    def predicts(self, test_data, img_name, real_width, real_height, save_path="result"):
        batch_size, _, _, _ = np.shape(test_data)
        assert len(img_name) == batch_size
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        predicted = self.model(test_data)

        for i in range(batch_size):
            recovery_img = (predicted[i] * 127.5 + 127.5).numpy().astype(np.uint8)
            recovery_img = Image.fromarray(recovery_img)
            recovery_img = recovery_img.resize([real_width[i], real_height[i]], Image.ANTIALIAS)
            recovery_img.save(save_path + "/{}".format(img_name[i]))
        return predicted

    def predict(self, test_data, real_width, real_height, save_name="result.jpg", save_path="result"):
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        predicted = self.model(test_data)
        predicted = tf.squeeze(predicted, axis=0)

        recovery_img = (predicted * 127.5 + 127.5).numpy().astype(np.uint8)
        recovery_img = Image.fromarray(recovery_img)
        recovery_img = recovery_img.resize([real_width, real_height], Image.ANTIALIAS)
        recovery_img.save("{}/{}".format(save_path, save_name))

        return recovery_img


class Discriminator(Model):

    def __init__(self, input_shape):
        super().__init__()
        input_layer = Input(shape=input_shape)

        model = Conv2D(filters=64, kernel_size=3, strides=1, padding="same")(input_layer)
        model = LeakyReLU(alpha=0.2)(model)

        model = DiscBlock(model, 3, 64, 2)
        model = DiscBlock(model, 3, 128, 1)
        model = DiscBlock(model, 3, 128, 2)
        model = DiscBlock(model, 3, 256, 1)
        model = DiscBlock(model, 3, 256, 2)
        model = DiscBlock(model, 3, 512, 1)
        model = DiscBlock(model, 3, 512, 2)

        model = Flatten()(model)
        model = Dense(1024)(model)
        model = LeakyReLU(alpha=0.2)(model)

        model = Dense(1)(model)
        model = Activation('sigmoid')(model)

        self.model = Model(inputs=input_layer, outputs=model)

    def __call__(self, input, training=None):
        return self.model(input, training=training)

    def summary(self):
        return self.model.summary()


class VGG_model(Model):
    def __init__(self, weight_path="VGG_pretrained.h5", input_shape=(64, 64, 3), is_trained=False):
        super().__init__()

        if not is_trained:
            vgg19 = tf.keras.applications.VGG19(weights="imagenet", include_top=False, input_shape=input_shape)
        else:
            vgg19 = tf.keras.applications.VGG19(weights=weight_path, include_top=False)

        self.model = Model(vgg19.input, vgg19.get_layer('block5_conv4').output)

    def __call__(self, input):
        return self.model(input)