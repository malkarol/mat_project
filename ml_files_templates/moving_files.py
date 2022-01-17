import shutil
import os
import random

source = '/Users/michal/Downloads/CIFAR-10-images-master/test/'
count = 1

directories = os.listdir(source)

while count!=100:
    dir = random.choice(directories)
    while dir ==".DS_Store":
        dir = random.choice(directories)
    files = os.listdir(source+dir+"/")
    file = random.choice(files)
    target ="/Users/michal/Desktop/cifar10/test/"+dir+"/"
    if not os.path.exists("/Users/michal/Desktop/cifar10/test/"+dir+"/"):
        os.makedirs("/Users/michal/Desktop/cifar10/test/"+dir+"/")
    shutil.move(source+dir+"/"+file, target)
    count=count+1

# count = 0
# for f in files:
#     if (count<300):
#         shutil.move(f, dest1)
print(directories)