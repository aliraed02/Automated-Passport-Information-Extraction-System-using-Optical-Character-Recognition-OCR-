# import library
import pytesseract
import pkg_resources
import cv2
from PIL import Image
import re


# declaring the exe path for tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# printing the tesseract version
#print(pkg_resources.working_set.by_key['pytesseract'].version)


# printing the opencv version
#print(cv2.__version__)



# loading the image from disk
img_to_ocr = cv2.imread(r"C:\Users\dc\OneDrive\Desktop\passport.jpg")

#print(img_to_ocr.shape)
# Preprocessing the image
# step 1: convert to gray scale
resize = cv2.resize(img_to_ocr, (1000, 658))
#print(resize.shape)
preprocessing_img = cv2.cvtColor(img_to_ocr, cv2.COLOR_BGR2GRAY)
# step 2: Do binary and otsu thresholding
preprocessing_img = cv2.threshold(preprocessing_img, 0,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# step3: Smooth the image using median blur
#preprocessing_img = cv2.medianBlur(preprocessing_img, 3)


# save the preprocessed image temporarily into the disk
cv2.imwrite('temp_img.jpg', preprocessing_img)


# read the temp image from disk as pil image
preprocessed_pil_img = Image.open('temp_img.jpg')


# pass the pil image to resseract to do OCR
text_extracted = pytesseract.image_to_string(preprocessed_pil_img)


# print the text
#print(text_extracted)

data = {}

for index, value in enumerate(text_extracted.splitlines()):
    #print(f'index = {index} \t value = {value}')
    try:
        if index == 3:
            passNo = [i for i in value.split()]
            data['PassportNo'] = passNo[-1]
        
        
        if index == 7:
            data['Name'] = value
           
            
        if index == 11:
            country = [i for i in value.split('/')]
            data['Nationality'] = country[-1]
            
            
            
        if index == 15:
            date = [i for i in value.split()]
            data['Date'] = date[0] + '/' + date[1][:3].upper() + '/' + date[2]
            pattern = r'[^a-zA-Z0-9\s]'
            filtered_text = re.sub(pattern, '', date[3])
            data['Gender'] = filtered_text
        
    except Exception as e:
        print("Error ", e)



    




print(data)
# display the original image

cv2.imshow('Actual Image', img_to_ocr)
cv2.waitKey(0)
cv2.destroyAllWindows()









