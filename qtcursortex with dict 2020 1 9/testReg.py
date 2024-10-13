import re 

s= '"f o o"'
x = re.sub('[^A-Za-z0-9]+', "", s)
print(x) 

