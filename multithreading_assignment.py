import os
import threading
from queue import Queue

full_path='./data'
queue_list=Queue()

# look for jpg file paths with jpg extension and add it to list
def read_from_directory(data):
    '''
    Take path as input
    Returns list containing names of image file with jpg extension
    '''

    for entry in os.listdir(data):

        if os.path.isfile(os.path.join(data,entry)):
            pathname=os.path.join(data,entry)
            a=pathname.endswith('.jpg')
            if a:
                queue_list.put(pathname)

        if os.path.isdir(os.path.join(data,entry)):
            read_from_directory(os.path.join(data,entry))

# add data to file
def add_to_file(data,name_of_file):
    '''
    Takes list as an input
    Writes data to file
    '''
    while True:
        name_of_file.write(queue_list.get()+'\n')


if __name__=='__main__':
    file1 = open('data.txt', 'a')

    t1=threading.Thread(target=read_from_directory,args=(full_path,))
    t2=threading.Thread(target=add_to_file,args=(queue_list, file1))

    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    file1.close()