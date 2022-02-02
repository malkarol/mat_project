import shutil
import os
import random

source = '/Users/michal/Desktop/covid/'
count = 1

directories = os.listdir(source)


# moving to test
while count != 1500:
    dir = random.choice(directories)
    while dir ==".DS_Store" or len(os.listdir(source+dir+"/"))==0:
        dir = random.choice(directories)
    files = os.listdir(source+dir+"/")
    file = random.choice(files)
    target =f"/Users/michal/Desktop/covid 2.02/test/"+dir+"/"
    if not os.path.exists(target):
        os.makedirs(target)
    shutil.move(source+dir+"/"+file, target)
    count += 1

# # moving to datasets
for i in range(1,4):
    for j in range(1, 6):
        count = 0
        while count != 200:
            dir = random.choice(directories)
            while dir ==".DS_Store" or len(os.listdir(source+dir+"/"))==0:
                dir = random.choice(directories)
            files = os.listdir(source+dir+"/")
            file = random.choice(files)
            target =f"/Users/michal/Desktop/covid 2.02/dataset{i}/part{j}/"+dir+"/"
            if not os.path.exists(target):
                os.makedirs(target)
            shutil.move(source+dir+"/"+file, target)
            count += 1

# moving to datasets unbalanced
for i in range(1,4):
    for j in range(1, 6):
        count = 0
        while count != 200:
            if i == 1:
                dir = 'Normal'
            elif i == 2:
                dir = 'COVID'
            else:
                dir = 'Lung_Opacity'
            while dir ==".DS_Store" or len(os.listdir(source+dir+"/"))==0:
               break
            files = os.listdir(source+dir+"/")
            print(len(files))
            file = random.choice(files)
            target =f"/Users/michal/Desktop/covid 2.02/dataset{i}/part{j}/"+dir+"/"
            if not os.path.exists(target):
                os.makedirs(target)
            shutil.move(source+dir+"/"+file, target)
            count += 1


# count = 0
# while count != 184:
#     source=f"/Users/michal/Desktop/covid 2.02/additional/"
#     dir = "COVID"
#     while dir ==".DS_Store" or len(os.listdir(source+dir+"/"))==0:
#         break
#     if len(os.listdir(source+dir+"/"))==0:
#         print(f'Count: {count}')
#         break
#     files = os.listdir(source+dir+"/")
#     file = random.choice(files)
#     target =f"/Users/michal/Desktop/covid 2.02/dataset2/part5/"+dir+"/"
#     if not os.path.exists(target):
#         os.makedirs(target)
#     shutil.move(source+dir+"/"+file, target)
#     count += 1
# #
for i in range(1,4):
    for j in range(1, 6):
        target =f"/Users/michal/Desktop/covid 2.02/dataset{i}/part{j}/"
        length = sum([len(files) for r, d, files in os.walk(f"/Users/michal/Desktop/covid 2.02/dataset{i}/part{j}/")])
        print(f'num of files for dataset{i}, part{j}: {length}')

