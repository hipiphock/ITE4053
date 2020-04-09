import numpy as np
import random
import math
from typing import List, Any

# KEY: just do W[2]a[1] for one hidden layer,

# INITAILIZATION
MIN_NUMBER = 1e-6

m = 1000
n = 100

alpha = 0.01 # learning rate
loss = 0

W1 = np.array([0, 0])
W2 = 0
b = 0

# data generator
def generate_random_data(size):
    X = []
    Y = []
    for i in range(size):
        x1 = random.randint(-2, 2)
        x2 = random.randint(-2, 2)
        if x1 + x2 > 0:
            Y.append(1)
        else:
            Y.append(0)
        X.append(np.array([x1, x2]))
    return X, Y

# Sigmoid function
def sigmoid(val):
    return 1/(1+math.exp(-val))

# Loss function for Logistic Regression
def L(a, y):
    return -(y*math.log(a) + (1-y)*math.log(1-a))

# training function
def train_vectorized(X, Y):
    global W1, W2, b, m, n
    batch_dW1 = np.array([0, 0])
    batch_dW2 = 0
    batch_db = 0
    for Xi, Yi in zip(X, Y):
        z = np.dot(W1, Xi) + b
        a = sigmoid(z)
        da = -Yi/a + (1-Yi)/(1-a)
        dz = da * a * (1-a) # == a-Yi
        dW1 = Xi*dz*W2
        dW2 = a
        db = dz*W2
        batch_dW1 = batch_dW1 + dW1/m
        batch_dW2 = batch_dW2 + dW2/m
        batch_db += db/m
    W1 = W1 - alpha*batch_dW1
    W2 = W2 - alpha*batch_dW2
    b = b - alpha*batch_db

def forward(Xi):
    global W1, b
    z = np.dot(W1, Xi) + b
    a = sigmoid(z)
    MIN_VAL = 1e-10
    a = max(a, MIN_VAL)
    a = min(a, 1 - MIN_VAL)
    return a

def loss_with_vectorization(X, Y):
    batch_loss = 0
    for i in range(len(X)):
        pred_y = forward(X[i])
        batch_loss -= Y[i] * math.log(pred_y) + (1 - Y[i]) * math.log(1 - pred_y)
    batch_loss /= len(X)
    return batch_loss

def accuracy_with_vectorization(X, Y):
    num_correct = 0
    for i in range(len(X)):
        z = np.dot(W1, X[i]) + b
        a = sigmoid(z)
        if Y[i] == round(forward(X[i])):
            num_correct += 1
    return num_correct/len(X)

def print_vectorized_w_b():
    print('w1: {}, w2: {}, b: {}'.format(W1[0], W1[1], b))

if __name__ == '__main__':
    train_X, train_Y = generate_random_data(m)
    test_X, test_Y = generate_random_data(n)
    for i in range(m):
        train_vectorized(train_X, train_Y)
        # print("Iteration: "+ i.__str__())
    print('W1_1: {}, W1_2: {}, W2: {}, b: {}'.format(W1[0], W1[1], W2, b))
    print('train_vectorized loss: {}, accuracy: {}'.format(loss_with_vectorization(train_X, train_Y), accuracy_with_vectorization(train_X, train_Y)))
    print('test loss: {}, accuracy: {}'.format(loss_with_vectorization(test_X, test_Y), accuracy_with_vectorization(test_X, test_Y)))