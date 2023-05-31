import os
import pdfplumber

def extractTextFromPdf(locationTuple):
    """ Read in the pdf, write file with the text
        Returns location of the file
    """
    pdfFile = locationTuple[0]
    txtFile = locationTuple[1]

    #In this project, we don't care about pages; we just want the full text as one long file
    allText = ''
    try:
        with pdfplumber.open(pdfFile) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text != '':
                    allText = allText + ' ' + text
            
        with open(txtFile, 'w', encoding = 'utf-8') as f:
            f.write(allText)
            
        return(txtFile)
                
    except Exception as e:
        print(f"Conversion failed for: {pdfFile} - Error: {e}", flush=True)
        return(f"Failed: {pdfFile}")
        
def createPdfList(dirs, textDir):
    """ To make paralel processing easier, we create a list of the location of all pdf files
        Input a list of folders, outputs a list of tuples: (pdf location, intended txt location)
    """
    listOfDirs = []
    for pdfDir in dirs:
        for file in os.listdir(pdfDir):
            if file.endswith('.pdf'):
                #The matching txt would be:
                outFile = os.path.join(textDir, f"{file.rsplit('.', 1)[0]}.txt")
                
                #As we are combining different dirs, file names may overlap
                if os.path.isfile(outFile): #if it already exists, add a number at the beginning
                    n = 0
                    while os.path.exists(outFile):
                        outFile = os.path.join(textDir,f"{n}dup_{file.rsplit('.', 1)[0]}.txt")
                        n+=1
                        if n>99:
                            print(f"Cannot find new file location for {outFile}\nOverwriting!", flush=True)
                            break
                
                listOfDirs.append(
                    (os.path.join(pdfDir, file), outFile)
                    )
                
    return(listOfDirs)