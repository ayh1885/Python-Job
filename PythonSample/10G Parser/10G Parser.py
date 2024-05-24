import re

def extract_hex_values_from_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        log_data = file.read()

    # 줄 단위로 데이터를 분리
    lines = log_data.split('\n')
    hex_data_lines = []
    block_number = 1
    for line in lines:
        # 날짜로 시작하는 줄은 무시
        if re.match(r'^[A-Za-z]{3}', line):
            continue
        if re.match(r'\n', line):
            hex_data_lines.append('\n')

        if re.match(r' 00 : ', line):
            hex_data_lines.append('\n--- NO.{} -------------------------------------------------\n'.format(block_number))
            block_number += 1

        # 'xx :' 패턴을 찾아서 제거하고 hex 값만 추출
        cleaned_line = re.sub(r'\b(?:\d{2}|\d{3}|[A-F0-9]{2}) :', '', line)

        # hex 값 뒤의 텍스트 제거
        hex_values = re.findall(r'([0-9A-F]{2})\s', cleaned_line)  # 'line' 대신 'cleaned_line' 사용
        if hex_values:
            hex_data_lines.append(' '.join(hex_values))

    extracted_hex_data = '\n'.join(hex_data_lines)

    with open(output_file_path, 'w') as file:
        file.write(extracted_hex_data)

# 예제 사용
input_file_path = 'INPUT_EONTMD'  # 로그 데이터가 저장된 입력 파일 경로
output_file_path = 'OUTPUT_EONTMD'  # 추출된 hex 데이터를 저장할 출력 파일 경로

# 함수를 사용하여 파일에서 hex 값 추출 후 다른 파일에 저장
extract_hex_values_from_file(input_file_path, output_file_path)