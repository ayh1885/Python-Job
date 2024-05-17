



'''
Exceptions, Warnings, and Log messages
pypdf makes use of 3 mechanisms to show that something went wrong:

[Log messages] are informative messages that can be used for post-mortem analysis. Most of the time, users can ignore them. They come in different levels, such as info / warning / error indicating the severity. Examples are non-standard compliant PDF files which pypdf can deal with or a missing implementation that leads to a part of the text not being extracted.

[Warnings] are avoidable issues, such as using deprecated classes / functions / parameters. Another example is missing capabilities of pypdf. In those cases, pypdf users should adjust their code. Warnings are issued by the warnings module - those are different from the log-level “warning”.

[Exceptions] are error-cases that pypdf users should explicitly handle. In the strict=True mode, most log messages with the warning level will become exceptions. This can be useful in applications where you can force to user to fix the broken PDF.

'''


#  https://pypdf.readthedocs.io/en/stable/user/metadata.html

#####################################
#       Reading MetaData
#####################################

from pypdf import PdfReader

reader = PdfReader("RELNOTES-SDK-6.4.5.pdf");

meta = reader.metadata
print(len(reader.pages))

# All of the following could be None!
print(meta.author)
print(meta.creator)
print(meta.producer)
print(meta.subject)
print(meta.title)


print("\n\n####################################################\n\n\n\n");


####################################
#   Extract Text from a PDF
####################################

page = reader.pages[0]
print(page.extract_text())

print("\n\n\n\n");

page = reader.pages[90]
print(page.extract_text())


print("\n\n\n\n");




def remove_footer(extracted_texts: list[str], page_labels: list[str]):
    def remove_page_labels(extracted_texts, page_labels):
        processed = []
        for text, label in zip(extracted_texts, page_labels):
            text_left = text.lstrip()
            if text_left.startswith(label):
                text = text_left[len(label) :]

            text_right = text.rstrip()
            if text_right.endswith(label):
                text = text_right[: -len(label)]

            processed.append(text)
        return processed

    extracted_texts = remove_page_labels(extracted_texts, page_labels)
    return extracted_texts



#print(remove_footer(page))

# extract text in a fixed width format that closely adheres to the rendered
# layout in the source pdf
#print(page.extract_text(extraction_mode="layout"))

# extract text preserving horizontal positioning without excess vertical
# whitespace (removes blank and "whitespace only" lines)
#print(page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False))

# adjust horizontal spacing
#print(page.extract_text(extraction_mode="layout", layout_mode_scale_weight=1.0))

# exclude (default) or include (as shown below) text rotated w.r.t. the page
#print(page.extract_text(extraction_mode="layout", layout_mode_strip_rotated=False))


print("\n\n####################################################\n\n\n\n");