Create a dataset using recipe related pdfs

Extracting text from pdf with the help of OCR dosen’t always gives good results that is why with the help of some python library first we need to determine the quality of a pdf and if it is good then only apply OCR on it or else don’t consider that pdf.


1. Build a PDF Scorer

Textract documentation link:  https://textract.readthedocs.io/en/latest/

With the help of textract we extracted texts from pdf and removed punctuations and numbers from the string so that we will simple get the text. Converted this into a list and then created a dictionary of each word from the list as a key and value as a number of occurence of that word in the whole pdf. Compared every word from dictionary with list of english words provided by nltk libraby. 
Calculated presence of each word and total word count from that pdf.  And calculated percentage of accuracy of each pdf.  

This helps in determining the quality of a pdf. If a quality of a pdf is good it then textract will extract texts correctly and most of the words will match with the english words present in the nltk library thus having good score 

2. Convert pdf with score into a dataset

Used pdf2image library to convert each pdf pages into images.
To each image we applied few image preprocessing techniques by which it will divide image into multiple boxes and for each box we can check if it matches certain conditions then it is a box contatining method or ingredients. We get contours from bottom to top that is why first we extracted last box which will contain title and applied OCR on it using pytesseract-(https://pypi.org/project/pytesseract/ )   and removed first two boxes which includes page number and footer in that image. And for rest for the boxes we are checking if it matches specified conditions

3. Title, ingredients and method data will be stored in a dictionary which will be used to add data into mongodb,

4. Read the data from mongdb and add it into csv file
