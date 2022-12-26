# -*- coding: utf-8 -*-
"""Final414_2Haylin

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kv0JFNblwOzHGHJSdH0WCO7gTXclLh1P
"""

"""
Haylin Diaz CMP414 Final Project
Creating and then testing a neural network without NN libraries
"""
class network:

  #Initializing random weight & bias parameters for model
  def init_params():
  #This example contains 1 hidden layer with 
  # 2 neurons (W1 and b1, W2 and b2)

    #When I tried to remove the -0.5 and change randn to rand,
    # i got errors in the epochs/iterations
      W1 = np.random.rand(10, 784) - 0.5
      #Generate random values from 1-10
      b1 = np.random.rand(10, 1) - 0.5 
      W2 = np.random.rand(10, 10) - 0.5
      b2 = np.random.rand(10, 1) - 0.5
      return W1, b1, W2, b2

  #Relu activation from scratch
  def Relu(Z):
      return np.maximum(Z, 0)

  #Defining softmax to calulate output (as probability)
  def softmax(Z):
      A = np.exp(Z) / sum(np.exp(Z))
      return A

  #Forward propagation
#RUBRIC - 3.`predict`: Calculates the output values for a list of input data.
  def feed_forward(W1, b1, W2, b2, X):
      #Calculating output using input, weights & biases
      Z1 = W1.dot(X) + b1
      #Activate using Relu as activation function
      A1 = network.Relu(Z1)
      Z2 = W2.dot(A1) + b2
      #Getting probability output
      A2 = network.softmax(Z2)
      return Z1, A1, Z2, A2

  #Finding derivative for backwards prop. 
  # booleans can convert to 1 or 0
  def Relu_deriv(Z):
      return Z > 0

  # ONE-HOT Encoding - Coverting/encoding previous output
  # for backwards prop
  def encode(Y):
    encode_Y = np.zeros((Y.size, Y.max() + 1))
    #Encode by converting row specified by Y to 1
    encode_Y[np.arange(Y.size), Y] = 1
    encode_Y = encode_Y.T
    return encode_Y

  #Backwards prop. to evaluate best paramters using previous output
  def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
      m = Y.size
      encode_Y = network.encode(Y)
      dZ2 = A2 - encode_Y
      dW2 = 1 / m * dZ2.dot(A1.T)
      db2 = 1 / m * np.sum(dZ2)
      #Applying weights in reverse
      dZ1 = W2.T.dot(dZ2) * network.Relu_deriv(Z1)
      #Booleans can convert to 1 or 0 for multip.

      dW1 = 1 / m * dZ1.dot(X.T)
      db1 = 1 / m * np.sum(dZ1)
      return dW1, db1, dW2, db2

  #Update new weight/bias values evaluated by backwards prop.
  def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, a):
      W1 = W1 - a * dW1
      b1 = b1 - a * db1    
      W2 = W2 - a * dW2  
      b2 = b2 - a * db2    
      #Return new/update parameters
      return W1, b1, W2, b2

  def get_accuracy(predictions, Y):
      print(predictions, Y)
      #Evaluating output by counting correct predictions
      return np.sum(predictions == Y) / Y.size

  def get_predictions(A2):
      return np.argmax(A2, 0)

  #Train model using stochastic gradient descent
  def fit(X, Y, a, iterations):
      #initialize wieght/bias params for new model
      W1, b1, W2, b2 = network.init_params()

      for i in range(iterations):
        #Loop of Calulating output by feeding forward,
        # evaluating ouput & weight/bias parameters using backwards prop., and
        # then updating better evaluated params
          Z1, A1, Z2, A2 = network.feed_forward(W1, b1, W2, b2, X)
          dW1, db1, dW2, db2 = network.backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
          W1, b1, W2, b2 = network.update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, a)
          #Show iteration # and accuracy every 25 iterations
          if i % 25 == 0:
              print("Iteration: ", i)
              predictions = network.get_predictions(A2)
              print(network.get_accuracy(predictions, Y))
      return W1, b1, W2, b2

#Numpy will still be needed for math/linear algebra operations
import numpy as np
#Pandas will still  be needed for reading data to use the network
import pandas as pd
#NO Tensorflow/Keras

#Using pandas to read sample mnist dataset
mnist_data = pd.read_csv('mnist_train_small.csv')

#Changing data from pandas dataframe into
# a numpy array of values makes it easier to 
# mathematically manipulate the data with numpy
mnist_data = np.array(mnist_data)

#Getting the dimensions of the dataset
m, n = mnist_data.shape

#Shuffling data before splitting into 
# regular training set and validation set
np.random.shuffle(mnist_data) 

#Splitting data without using test_train_split
val_data = mnist_data[0:1000].T 
#Transposing this would be easier to understand 
# and work with since there are 700+ pixel values
# representing one row/example

#Column of correct labels for validation later
Y_validation = mnist_data[0] 
X_validation = val_data[1:n]
#Dividing into float values to make them readable as pixels
X_validation = X_validation / 255.

#Training data
data_train = mnist_data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.

#Calling a model to test on sample mnist data set
# mnist train/test data as params, 500 iterations for fit loop
W1, b1, W2, b2 = network.fit(X_train, Y_train, 0.10, 500)