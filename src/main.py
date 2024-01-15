import torch
import matplotlib.pyplot as plt
import torch.optim as opt
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from modules.cnn import CNN

# Root path to datasets
PATH = "C:/Users/Ato/Documents/Programming/Python/catdog/src/datasets"

# Select GPU if available (cuda toolkit <= 11.8 for pytorch)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(f"Training on device: {device}")


# Hyperparameters
batch_size = 16
lr = 0.001
momentum = 0.9
epochs = 2

# Transforms for training set
train_transform = transforms.Compose([
  transforms.Resize((256,256)),
  transforms.ToTensor(),
])

# Data Loader with transformations, batch size and shuffle
train_path = PATH + "/train"
train_set = datasets.ImageFolder(root=train_path, transform=train_transform)
train_loader = DataLoader(train_set, batch_size=16, shuffle=True)

'''
# Image test #
# - Manually iterates through the batch and shows the first image.
# - permute() changes the order of dimensions so the Channel (RGB) is in the last position.
images, labels = next(iter(train_loader))
plt.imshow(images[0].permute(1,2,0).numpy())
plt.show() # No need if using notebooks

# Debug tensors and numpy image representation
print("TENSOR: ", images[1])
print("NUMPY: ", images[1].numpy())
'''

cnn = CNN(batch_size).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = opt.SGD(cnn.parameters(), lr, momentum)

for epoch in range(epochs):
  running_loss = 0.0
  for i, data in enumerate(train_loader, 0):
    imgs, labels = data
    imgs, labels = imgs.to(device), labels.to(device)

    # Forward + backward + optimize
    output = cnn(imgs)
    loss = criterion(output, labels)
    loss.backward()
    optimizer.step()

    # print statistics
    running_loss += loss.item()
    print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2:.3f}')
    running_loss = 0.0

print('Finished Training')




