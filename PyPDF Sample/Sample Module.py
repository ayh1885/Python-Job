

from pypdf import PdfReader

reader = PdfReader("RELNOTES-SDK-6.4.5.pdf")




def ParseAllString(PageString: str):

    for str in PageString.strip():
        if(str == "Rlease"):
            print(str)
            break





    return


for i in range(90, 91):
    page = reader.pages[i]
    PageString = page.extract_text()

    print(PageString + "\n\n")
    ParseAllString(PageString)



