
import torch.nn as nn
# Implementation of the SmileCNN which stops at the feature extraction layer
class SmileCNNSVM(nn.Module):
  def __init__(self):
    super(SmileCNNSVM, self).__init__()
    # Define the convolutional layers
    self.conv1 = nn.Conv2d(1, 16, kernel_size=9)
    self.conv2 = nn.Conv2d(16, 8, kernel_size=5)
    self.conv3 = nn.Conv2d(8, 16, kernel_size=5)

    # Define the max pooling layers
    self.pool1 = nn.MaxPool2d(kernel_size=2)
    self.pool2 = nn.MaxPool2d(kernel_size=2)
    self.pool3 = nn.MaxPool2d(kernel_size=2)

    # Define the fully connected layer
    #self.fc = nn.Linear(400, 400)
    self.out = nn.Linear(256, 2)
    self.flatten = nn.Flatten()

    self.relu = nn.ReLU()
    #self.flatten - nn.Flatten()
    self.dropout = nn.Dropout(0.5)

  def forward(self, x):
    x = self.conv1(x)
    x = self.pool1(self.relu(x))
    x = self.conv2(x)
    x = self.pool2(self.relu(x))
    x = self.conv3(x)
    x = self.dropout(x)
    x = self.pool3(self.relu(x))    

    x = self.flatten(x)
    w = x
    x = self.out(x)
    return x, w