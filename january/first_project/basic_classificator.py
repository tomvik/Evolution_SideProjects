# TensorFlow and tf.keras.
import tensorflow as tf
from tensorflow import keras

# Helper libraries.
import numpy as np
import matplotlib.pyplot as plt

print('TensorFlow Version: ', tf.__version__)

show_first_image = True
verify_first_25_images = True


def plot_image(i, predictions_array, true_label, img):
	predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
	plt.grid(False)
	plt.xticks([])
	plt.yticks([])

	plt.imshow(img, cmap=plt.cm.binary)

	predicted_label = np.argmax(predictions_array)
	if predicted_label == true_label:
		color = 'blue'
	else:
		color = 'red'
  
	plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
									100*np.max(predictions_array),
									class_names[true_label]),
									color=color)

def plot_value_array(i, predictions_array, true_label):
	predictions_array, true_label = predictions_array[i], true_label[i]
	plt.grid(False)
	plt.xticks([])
	plt.yticks([])
	thisplot = plt.bar(range(10), predictions_array, color="#777777")
	plt.ylim([0, 1]) 
	predicted_label = np.argmax(predictions_array)

	thisplot[predicted_label].set_color('red')
	thisplot[true_label].set_color('blue')




# Create Fashion_MNIST object.
fashion_mnist = keras.datasets.fashion_mnist

# I'll have two arrays of two arrays, Training{i,l} and Testing{i,l}.
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# There are 10 labels
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Print out shape of training arrays
print('Shape of training dataset: ', train_images.shape)
print('Lenght of training labels: ', len(train_labels))

# Print out shape of testing arrays
print('Shape of testing dataset: ', test_images.shape)
print('Lenght of testing labels: ', len(test_labels))

if show_first_image:
	plt.figure()
	plt.imshow(train_images[0])
	plt.colorbar()
	plt.grid(False)
	plt.show()
	input("Press Enter to continue...")

# We need the data from 0 to 1.
train_images = train_images / 255.0
test_images = test_images / 255.0


if verify_first_25_images:
	plt.figure(figsize=(10,10))
	for i in range(25):
		plt.subplot(5,5,i+1)
		plt.xticks([])
		plt.yticks([])
		plt.grid(False)
		plt.imshow(train_images[i], cmap=plt.cm.binary)
		plt.xlabel(class_names[train_labels[i]])
	plt.show()
	input("Press Enter to continue...")

# Create model
# Flatten the image to a 28*28 (784) array.
# First layer is 128 using ReLu
# Second and last layes is the 10 outputs and uses SoftMax to get class
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

# Compile model
# Using Adam Optimizer
# Normal loss function
# Its metrics will be accuracy
model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Feed the model with training dataset and separate it in 5 epochs.
# It also trains the model
model.fit(train_images, train_labels, epochs=5)

# Now, we test the trained model to evaluate its performance
test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)

# Predict results
predictions = model.predict(test_images)

# Plot the first X test images, their predicted label, and the true label
# Color correct predictions in blue, incorrect predictions in red
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
	plt.subplot(num_rows, 2*num_cols, 2*i+1)
	plot_image(i, predictions, test_labels, test_images)
	plt.subplot(num_rows, 2*num_cols, 2*i+2)
	plot_value_array(i, predictions, test_labels)
plt.show()
input("Press Enter to continue...")

# Grab an image from the test dataset
img = test_images[0]

print(img.shape)

# Add the image to a batch where it's the only member.
img = (np.expand_dims(img,0))

print(img.shape)

predictions_single = model.predict(img)

print(predictions_single)

plot_value_array(0, predictions_single, test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)

print('Final pred: ', np.argmax(predictions_single[0]))