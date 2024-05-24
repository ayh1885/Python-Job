from pypdf import PdfReader

reader = PdfReader("EPON_ONUxG-PG302-R26X-R33X-RDS - BRCM OAM Extension.pdf");

if reader.is_encrypted:
    reader.decrypt("docs788733")




print("########################################################################")
print("#\t\t\tBranch 7")
print("########################################################################")

print("\n\n\n\n");

for i in range(31, 41):
    page = reader.pages[i]
    PageString = page.extract_text()

    print(PageString + "\n\n\n\n")







print("\n\n\n\n\n\n")
print("########################################################################")
print("#\t\t\tBranch 9")
print("########################################################################")


print("\n\n\n\n");

page = reader.pages[105]
print(page.extract_text())



print("\n\n\n\n");

page = reader.pages[106]
print(page.extract_text())


print("\n\n\n\n");

page = reader.pages[107]
print(page.extract_text())





'''
print("\n\n\n\n");

page = reader.pages[27]
print(page.extract_text())
'''
