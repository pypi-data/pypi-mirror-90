def readpdf(pdf,page_number):        
        import pyttsx3 as pt
        a = pt.init()
        a.setProperty('rate', 150)
        import PyPDF2 as pd
        bo = open(pdf,'rb')
        pd_re = pd.PdfFileReader(bo)
        pages = pd_re.numPages
        #print(pages)
        for nu in range(page_number-1,pages):
            page = pd_re.getPage(nu)
            text = page.extractText()
            a.say(text)
            a.runAndWait()
