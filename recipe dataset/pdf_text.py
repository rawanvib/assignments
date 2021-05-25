import os
import cv2
import re
import pandas as pd
import csv
import pymongo
import pytesseract
from pdf2image import convert_from_path
import pdf_scorer
# from pdf2image.exceptions import (
#     PDFInfoNotInstalledError,
#     PDFPageCountError,
#     PDFSyntaxError
# )


def pdf_to_image(directory_path, list_pdfs):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for pdf in list_pdfs:
        pages = convert_from_path(pdf, 300, first_page=7, fmt='jpg')
        counter = 1
        pdf_file_name = os.path.splitext(pdf)[0]

        pdf_file_name = re.sub('/', '_', pdf_file_name)

        for page in pages:
            image_file_name = directory_path + pdf_file_name + '_' + str(counter) + '.jpg'
            counter = counter + 1
            page.save(image_file_name, 'JPEG')


def image_to_data(dir_name, col):
    for image_path in os.listdir(dir_name):
        image = cv2.imread(os.path.join(dir_name, image_path))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 5)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 25))

        dilation = cv2.dilate(thresh, rect_kernel, iterations=2)

        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        image2 = image.copy()

        box = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            box.append((x, y, x + w, y + h))

        box0 = box[-1]
        x, y, l, b = box0
        cropped = image2[y:b, x:l]
        text = pytesseract.image_to_string(cropped)

        single_document = {}

        single_document['title'] = text

        box = box[:-1]
        box = box[2:]

        ingredients = []
        method = []
        for i in range(len(box)):
            x, y, l, b = box[i]
            cropped = image2[y:b, x:l]

            # convert image into text
            text = pytesseract.image_to_string(cropped)

            # list of sentence
            word_list = text.split('\n')

            new_list = []
            for word in word_list:
                if word != '':
                    new_list.append(word)

            # to remove '\x0c'
            new_list = new_list[:-1]

            len_sentence = len(new_list)

            counter = 0
            for sentence in new_list:
                if sentence[0].isnumeric():
                    counter = counter + 1

            # if len_sentence == counter or len_sentence -1 == counter or len_sentence - 2 == counter or len_sentence - 3 == counter:
            if sentence[0].isupper():
                count_full_stop_method = 0
                for i in new_list:
                    search_return = re.findall(r"\.", i)
                    count_full_stop_method = count_full_stop_method + len(search_return)
                if count_full_stop_method >= len_sentence//2 or count_full_stop_method == len_sentence:
                    method.append(new_list)
                else:
                    if len_sentence == counter or len_sentence // 2 < counter:
                        ingredients.append(new_list)
                    else:
                        method.append(new_list)
            else:
                if len_sentence == counter or len_sentence // 2 < counter:
                    ingredients.append(new_list)
                else:
                    method.append(new_list)

        single_document['ingredients'] = ingredients
        single_document['method'] = method

        # print(single_document)
        document_to_db(single_document, col)
        single_document.clear()

def document_to_db(data, col):
    col.insert_one(data)

def db_to_csv(col, filename):
    list_data=list(col.find({}))
    df=pd.DataFrame(list_data)
    df.pop('_id')
    df.to_csv(filename, index=True)

if __name__ == '__main__':

    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = my_client['recipe_demo_changed_final3']
    my_col = my_db['dataset']

    csv_filename='db_csv.csv'

    image_directory = 'images_folder3/'
    directory_name = "/home/webwerks/Desktop/ocr/pdfs"

    pdf_with_score = pdf_scorer.path_to_pdf_file(directory_name)
    #print(pdf_with_score)
    list_pdf_with_good_score = []
    for pdf_file, score in pdf_with_score.items():
        if score > 82 :
            list_pdf_with_good_score.append(pdf_file)

    #print(list_pdf_with_good_score)
    pdf_to_image(image_directory, list_pdf_with_good_score)
    image_to_data(image_directory, my_col)
    db_to_csv(my_col,csv_filename)





