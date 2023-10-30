# DOGA CHALLENGE

This is our solution for a challenge provided by the Doga company.

### What is DOGA?

Doga is an international company that designs and manufactures components and systems for the automotive, industrial, and renewable energy sectors.

### Who is part of our team?

- Agustina aka [Aheredia](https://github.com/AgustinaHeredia)
- Fabian aka [fscorcel](https://github.com/42barcelonastudent)
- Zsolt aka [zpalfi](https://github.com/zpalfi42)

### What was the challenge?

DOGA presented us a database full of PDFs. They asked us if we could transform this PDFs into EXCEL format.

### Explanation of our solution

The first day we started analyzing all the PDFs and started extracting information from them. We used PyPDF2 in Python to extract all the text info from them, but we encountered a problem, sometimes the extracted text was nothing although the page was there full of information. We investigated why this was happening and we discover that some PDF's where scanned! Yes, they were images.

To solve this problem, we started using PyTesseract and PDF2Image, which was working fine but sometimes instead of extracting the number 1 we were extracting the number 4 and PyTesseract was extracting the information a little bit weirdly... So we made a few changes, we augmented the quality of pdf2image ass well as the PyTesseract PSM (Page Segmentation Mode) and the OEM (OCR Engine Mode). 

With these changes all was working well, we extracted all the text and started extracting the different information DOGA wanted. We achieved around 60% of success with this method, but we felt something out of place, we did not like the speed of our solution, so we investigated different solutions and found that the problem was PyTesseract.

Every time we called the PyTesseract function it had to call the trained model, start in and then read the image. We where sure it existed another solution, so we went thought, why we dont use the model directly? That's what we did, we used the Tesseract API so we dont have to start the model every time we wanted to extract information, we just had to start it once at the begining. With this change it was a lot faster but we didn't want 60% of success, we wanted more, so we started cleaning all the extracted info and increasing our success rate. We arived at 95% succes rate when the PDF was all text and 85% when it was scanned, why not 100%? 

We think that 100% succes rate is impossible, why? Because of the PDF's format. We found that some of the values we had to extraxt weren't aligned with it's keyword, so for the Tesseract OCR it was impossible to read it in the right order. This added to Tesseract still having some fails while reading the image is why we are very happy with having the 85-95% os succes rate.

We ended the challenge by doing a simple interface user-friendly to simplify the selection of folder or a PDF.

### Future ideas

We thought of implementing a keyword detector to detect certains keywords so the DOGA team would have easier to search for a certain PDF based on that keyword. We also wanted to implement the option of creating a new EXCEL or append to a EXCEL that alredy exist. And the last one thing we thought of implementing is to be able to execute this program with Docker, we didn't have time to investigate how to work with a visual interface in Docker.

### The result

We ended winning the second place, although we had the best results.

### Gretings

Thanks to DOGA for giving us the chance to impove our skills while helping you with this problem. Thanks also to my teammates for the incredible work they've done. And thank's to 42 school for bringing this types of chalenges.
