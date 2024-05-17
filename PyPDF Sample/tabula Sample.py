
import tabula

# PDF 파일에서 표 데이터 추출
file_path = "C:/Users/UBI-1072/Desktop/PracticePython/PyPDF Sample"
df = tabula.read_pdf(file_path)