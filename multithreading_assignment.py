import os
import glob
import threading
import pandas
import csv


full_path='./data'
image_file=[]

def file(path,file):  
    image=glob.glob(os.path.join(path,'*.jpg'))
    image_file.append(image)


def directory(path):
    for i in os.scandir(path):
        if i.is_file():
            print(i)
            file(path,i)
        if i.is_dir():
            print(i)
            directory(i)

def add_to_csv(data):
        with open('innovators1.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerows(data)

if __name__=='__main__':
    t1=threading.Thread(target=directory(full_path))
    t2=threading.Thread(target=add_to_csv(image_file))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    print(len(image_file))
