'''
Get number of data points(number of files) for a given directory and its subdirectories.
RUN ONCE, when user needs to know how large his/hers dataset is.
'''
import os
cpt = sum([len(files) for r, d, files in os.walk("/Users/michal/Documents/trainingSet/")])
print(cpt-1)