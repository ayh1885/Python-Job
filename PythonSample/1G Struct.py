




class _1G_MSG:

    def __init__(self, _String: str):

        Strings = _String.split(" ", 4)
        Result = [];
        for Strs in Strings:
            list = Strs.split("\n", 1);      # 해당 문제점이라고 할 수 있다면, 마지막 /r/n이 다를 수 있다... 하지만, 내가 \n 2번 넣도록 정해서 데이터 베이스에 정확이 넣기만 한다면 문제가 나지 않을 것이다.
            #list = Strs.split("\n");
            for Input in list:
                if Input == "":
                    continue
                Result.append(Input)

        self.Dst = Result[0];
        self.Src = Result[1];

        self.Len = Result[2][0:2];
        self.Type = Result[2][2:4];

        self.Subtype = Result[3];
        self.Flags = Result[4];
        self.Code = Result[5];

        """
        for Data in Result[6: len(Result)]:
            self.DataAndPad.append(Data);
        """

        for Data in Result[6:len(Result)]:
            self.DataAndPad += Data + "\n";



    def Print(self):
        print("Dst: " + self.Dst);
        print("Src: " + self.Src);

        print("Len: " + self.Len);
        print("Type: " + self.Type);

        print("Subtype: " + self.Subtype);
        print("Flags: " + self.Flags);
        print("Code: " + self.Code);

        print("DataAndPad: ");
        print(self.DataAndPad);



    def MatchTest(self, _Compare:str):

        return False;

        return True;



    Dst: str = "";      # 6Byte
    Src: str = "";      # 6Byte

    Len: str = "";      # 1Byte     # 이 Len/Type 이 원래 하나로서 2Byte이다.
    Type: str = "";     # 1Byte

    Subtype: str = "";  # 1Byte
    Flags: str = "";    # 2Byte
    Code: str = "";     # 1Byte


    #DataAndPad = [];   # 가변 42 ~ 1496..
    DataAndPad: str = "";



"""

TestString = "\n\
0180C2000002 00271CAFAFAB 8809\n\
03 0050\n\
FE 000db6\n\
00 67 24 00 13 25 80 32 80 32 4f 4e 54 2d 55 31\n\
30 34 43 54 00 00 00 00 00 00 00 00 00 00 00 00\n\
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n\
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n\
00 00 00 00 00 00 00 00 00 00 00 27 1c af af ab\n\
01 05 08 08 00 08 08 00 00 00 00 00 02 03 d8 04\n\
00 00 80 32\n\
\n\
\n\
"
print(TestString)

Strings = TestString.split(" ", 4)

Result = [];

for Strs in Strings:
    #list = Strs.split("\n", 1);      // 해당 문제점이라고 할 수 있다면, 마지막 /r/n이 다를 수 있다... 하지만, 내가 \n 2번 넣도록 정해서 데이터 베이스에 정확이 넣기만 한다면 문제가 나지 않을 것이다.
    list = Strs.split("\n");
    for Input in list:
        if Input == "":
            continue
        Result.append(Input)


print(Strings);
print(Result);



TEST1 = "1234"

aaa = TEST1[0:4]
print(aaa);


print("=================================================================")
print("=================================================================")
print("=================================================================")

Obj = _1G_MSG(TestString)
Obj.Print();

"""


MakeFile = open('1G HexaDumpData', 'r');

Input = "";
Count = 0;

while True:
    line = MakeFile.readline();
    if not line:

        print(Input);
        Obj = _1G_MSG(Input); Count += 1
        Obj.Print();
        break;

    if line.startswith("--- N0."):
        if Input == "":
            continue

        print(Input);
        Obj = _1G_MSG(Input); Count += 1
        Obj.Print();

        Input = "";
        continue;

    Input += line;

MakeFile.close();

print("End: " + str(Count))