from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import tensorflow.keras.backend as K
import tensorflow as tf
import cv2
from PIL import Image, ImageOps
from io import BytesIO
import base64
import numpy as np
import json

# Discriminator: Shared weights between the supervised classifier and standard discriminator 
# as found in GANs
# Reference: Chapter 20, GANs in Python by Jason Brownlee, Chapter 7 of GANs in Action

# Activation function for the discriminator as proposed in https://arxiv.org/abs/1606.03498

def custom_activation(output):
    logexpsum = K.sum(K.exp(output), axis=-1, keepdims=True)
    result = logexpsum / (logexpsum + 1.0)
    return result

def disc_network(in_shape=(50,50,3), n_classes=2):
    
    in_image = Input(shape=in_shape)
 
    fe = Conv2D(32, (3,3), strides=(2,2), padding='same')(in_image)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Conv2D(64, (3,3), strides=(2,2), padding='same')(fe)
    fe = BatchNormalization()(fe)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Conv2D(128, (3,3), strides=(2,2), padding='same')(fe)
    fe = BatchNormalization()(fe)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Conv2D(256, (3,3), strides=(2,2), padding='same')(fe)
    fe = BatchNormalization()(fe)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Dropout(0.4)(fe)
    fe = Flatten()(fe)

    fe = Dense(n_classes)(fe)

    # Supervised classifier
    c_out_layer = Activation('softmax')(fe)
    c_model = Model(in_image, c_out_layer)

    # Traditional discriminator as found in GANs
    d_out_layer = Lambda(custom_activation)(fe)
    d_model = Model(in_image, d_out_layer)

    return d_model, c_model

# Generator
# Reference: Chapter 20, GANs in Python by Jason Brownlee, Chapter 7 of GANs in Action
def generator_network(latent_dim):
    in_lat = Input(shape=(latent_dim,))

    n_nodes = 256 * 3 * 3
    gen = Dense(n_nodes)(in_lat)
    gen = Reshape((3, 3, 256))(gen)

    gen = Conv2DTranspose(128, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)

    gen = Conv2DTranspose(64, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = Conv2DTranspose(32, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = Conv2DTranspose(16, (3,3), strides=(1,1), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = Conv2DTranspose(8, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = ZeroPadding2D()(gen)
    
    out_layer = Conv2DTranspose(3, (3,3), strides=(1, 1), activation='tanh', padding='same')(gen)

    model = Model(in_lat, out_layer)

    return model



class GradCAM:
	def __init__(self, model, classIdx, layerName=None):
		# store the model, the class index used to measure the class
		# activation map, and the layer to be used when visualizing
		# the class activation map
		self.model = model
		self.classIdx = classIdx
		self.layerName = layerName

		# if the layer name is None, attempt to automatically find
		# the target output layer
		if self.layerName is None:
			self.layerName = self.find_target_layer()

	def find_target_layer(self):
		# attempt to find the final convolutional layer in the network
		# by looping over the layers of the network in reverse order
		for layer in reversed(self.model.layers):
			# check to see if the layer has a 4D output
			if len(layer.output_shape) == 4:
				return layer.name

		# otherwise, we could not find a 4D layer so the GradCAM
		# algorithm cannot be applied
		raise ValueError("Could not find 4D layer. Cannot apply GradCAM.")

	def compute_heatmap(self, image, eps=1e-8):
		# construct our gradient model by supplying (1) the inputs
		# to our pre-trained model, (2) the output of the (presumably)
		# final 4D layer in the network, and (3) the output of the
		# softmax activations from the model
		gradModel = Model(
			inputs=[self.model.inputs],
			outputs=[self.model.get_layer(self.layerName).output, 
				self.model.output])

		# record operations for automatic differentiation
		with tf.GradientTape() as tape:
			# cast the image tensor to a float-32 data type, pass the
			# image through the gradient model, and grab the loss
			# associated with the specific class index
			inputs = tf.cast(image, tf.float32)
			(convOutputs, predictions) = gradModel(inputs)
			loss = predictions[:, self.classIdx]

		# use automatic differentiation to compute the gradients
		grads = tape.gradient(loss, convOutputs)

		# compute the guided gradients
		castConvOutputs = tf.cast(convOutputs > 0, "float32")
		castGrads = tf.cast(grads > 0, "float32")
		guidedGrads = castConvOutputs * castGrads * grads

		# the convolution and guided gradients have a batch dimension
		# (which we don't need) so let's grab the volume itself and
		# discard the batch
		convOutputs = convOutputs[0]
		guidedGrads = guidedGrads[0]

		# compute the average of the gradient values, and using them
		# as weights, compute the ponderation of the filters with
		# respect to the weights
		weights = tf.reduce_mean(guidedGrads, axis=(0, 1))
		cam = tf.reduce_sum(tf.multiply(weights, convOutputs), axis=-1)

		# grab the spatial dimensions of the input image and resize
		# the output class activation map to match the input image
		# dimensions
		(w, h) = (image.shape[2], image.shape[1])
		heatmap = cv2.resize(cam.numpy(), (w, h))

		# normalize the heatmap such that all values lie in the range
		# [0, 1], scale the resulting values to the range [0, 255],
		# and then convert to an unsigned 8-bit integer
		numer = heatmap - np.min(heatmap)
		denom = (heatmap.max() - heatmap.min()) + eps
		heatmap = numer / denom
		heatmap = (heatmap * 255).astype("uint8")

		# return the resulting heatmap to the calling function
		return heatmap

	def overlay_heatmap(self, heatmap, image, alpha=0.5,
		colormap=cv2.COLORMAP_VIRIDIS):
		# apply the supplied color map to the heatmap and then
		# overlay the heatmap on the input image
		heatmap = cv2.applyColorMap(heatmap, colormap)
		output = cv2.addWeighted(image, alpha, heatmap, 1 - alpha, 0)

		# return a 2-tuple of the color mapped heatmap and the output,
		# overlaid image
		return (heatmap, output)

class Predictor(object):
    def predict(self, model, images_base64, image_shape, labels):
        responses = []
        #for base64Img in images_base64:
        for img_file_key, base64Img in images_base64.items():
            decoded_img = base64.b64decode(base64Img)
            img_buffer = BytesIO(decoded_img)
            imageData = Image.open(img_buffer).convert("RGB")
            
            img = ImageOps.fit(imageData, image_shape, Image.ANTIALIAS)
            img_conv = np.array(img)

            x_test = img_conv / 255.0
            x_test = np.expand_dims(x_test, 0)

            y_pred = model.predict(x_test)
            y_pred_prob = np.max(y_pred, axis=-1)
            y_pred = np.argmax(y_pred, axis=-1)
            
            class_idx = np.argmax(y_pred[0])    
            
            # initialize our gradient class activation map and build the heatmap
            cam = GradCAM(model, class_idx)
            heatmap = cam.compute_heatmap(x_test)

            # resize the resulting heatmap to the original input image dimensions
            # and then overlay heatmap on top of the image
            heatmap = cv2.resize(heatmap, image_shape)
            (heatmap, output) = cam.overlay_heatmap(heatmap, img_conv, alpha=0.5)
            print("heatmap :", heatmap)

            img = Image.fromarray(output, 'RGB')
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            base64_str = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("utf-8")

            resp = {img_file_key: [str(labels[y_pred[0]]), str(y_pred_prob[0]), base64_str]}
            responses.append(resp)
        return json.dumps(responses)
