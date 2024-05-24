
import os


'''
string_Data1 = "01020304"
string_Data2 = "01 02 03 04"

IntData = int(string_Data1, 16);
print(IntData)

#HexData = hex(string_Data1);
#print(HexData);

HexData = hex(IntData);
print(HexData);



def read_until_separator(filename, separator):
    try:
        with open(filename, 'r') as file:
            content = ''
            for line in file:
                if line.strip() == separator:
                    break
                content += line
            return content
    except FileNotFoundError:
        return f"파일 '{filename}'을(를) 찾을 수 없습니다."

# 사용 예시
filename = '1G HexaDumpData'  # 파일명을 적절히 변경하세요
separator = "--- "
result = read_until_separator(filename, separator)
print(result)

'''

a = 100
Dict = {}
List = []
for i in range(1, 100):

    if not a in List:
        Dict[a] = []
        print("???")
        List.append(a)

    Dict[a].append(i)

print(Dict)

try:
    os.mkdir("Test")
except FileExistsError:
    pass

TestFileOpen = open("Test/TestTestfile.txt", "a+")
TestFileOpen.write("Test\n\n")
TestFileOpen.close()



