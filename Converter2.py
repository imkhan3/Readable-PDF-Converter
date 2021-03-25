from pdf2image import convert_from_path
from PIL import Image
import cv2
import pytesseract
from PyPDF2 import PdfFileMerger
import os


pytesseract.pytesseract.tesseract_cmd= 'C://Program Files//Tesseract-OCR//tesseract.exe'
TESSDATA_PREFIX='C://Program Files//Tesseract-OCR'
tessdata_dir_config='--tessdata-dir "C://Program Files//Tesseract-OCR//tessdata"'

def convertPDF(infile,outfile):
    #PDF to image
    pages = convert_from_path(infile,thread_count=2, poppler_path=r'C:\Program Files\poppler-0.68.0\bin' )
    print("Beginning conversion")
    imageList = []
    pdfList = []
    for i, page in enumerate(pages):
        input_dir = 'image'+str(i)+'.jpg'
        output_dir = 'searchablePDF'+str(i)+'.pdf'
        
        page.save(input_dir, 'JPEG')
        imageList.append(input_dir)

    #Tesseract image to readable PDFs
        img = cv2.imread(input_dir,1)

        result = pytesseract.image_to_pdf_or_hocr(img, lang="eng",
        config=tessdata_dir_config)

        pdfList.append(output_dir)
        f = open(output_dir,"w+b")
        f.write(bytearray(result))
        f.close()
        print("page " + str(i+1)+" of " + str(len(pages)+1))
        
        
    #Merge PDF files
    merger = PdfFileMerger()
    print("Merging")
    for i in pdfList:
        merger.append(i)
    
    merger.write(outfile)
    merger.close()

    # Deleting created files
    for i in range(len(pdfList)):
        output_dir = 'searchablePDF'+str(i)+'.pdf'
        input_dir = 'image'+str(i)+'.jpg'
        f = open(input_dir)
        f.close()
        try:
            os.remove(input_dir)
            os.remove(output_dir)
        except OSError as e: # name the Exception `e`
            print ("Failed with to delete:", e.strerror) # look what it says
            print(f)

#Run function here
convertPDF("Paper1.pdf","result.pdf")