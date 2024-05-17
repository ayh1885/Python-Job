

class _1G_MSG:

    def __init__(self, _String: str):

        Strings = _String.split(" ", 4)
        Result = []
        for Strs in Strings:
            list = Strs.split("\n", 1)      # 해당 문제점이라고 할 수 있다면, 마지막 /r/n이 다를 수 있다... 하지만, 내가 \n 2번 넣도록 정해서 데이터 베이스에 정확이 넣기만 한다면 문제가 나지 않을 것이다.
            #list = Strs.split("\n");
            for Input in list:
                if Input == "":
                    continue
                Result.append(Input)

        self.Dst = Result[0]
        self.Src = Result[1]

        self.Len_Type = Result[2]

        self.Subtype = Result[3]
        self.Flags = Result[4]
        self.Code = Result[5]

        """
        for Data in Result[6: len(Result)]:
            self.DataAndPad.append(Data);
        """

        for Data in Result[6:len(Result)]:
            self.DataAndPad += Data + "\n"



    def Print(self):

        print("Dst: " + self.Dst)
        print("Src: " + self.Src)

        print("Len_Type: " + self.Len_Type)

        print("Subtype: " + self.Subtype)
        print("Flags: " + self.Flags)
        print("Code: " + self.Code)

        print("DataAndPad: ")
        print(self.DataAndPad)



    def MatchTest(self, _Compare:str):

        return False

        return True



    Dst: str = ""      # 6Byte
    Src: str = ""      # 6Byte

    Len_Type: str = ""  # 2Byte

    Subtype: str = ""  # 1Byte
    Flags: str = ""    # 2Byte
    Code: str = ""     # 1Byte


    #DataAndPad = [];   # 가변 42 ~ 1496..
    DataAndPad: str = ""




HexDumpDataFileName_PIU_16SC_1G = '1G HexaDumpData'


def DumpToHexData_PIU_16SC_1G(FileName:str):

    DumpFile = open(FileName, 'r')
    MakeFile = open(HexDumpDataFileName_PIU_16SC_1G, 'w')

    Num = 1

    while True:
        line = DumpFile.readline()
        if not line:
            break;
        # line.strip();

        PutStr = ""

        if line.startswith("D: "):
            MakeFile.write("--- N0." + str(Num) + " -------------------------------------------------\n\n")
            Num += 1;
            PutStr = line.split(" ")[1] + " " + line.split(" ")[3] + " " + line.split(" ")[5].replace("[", "").replace(
                "]", "")
        elif line.startswith("SubType: "):
            PutStr = line.split(" ")[1] + " " + line.split(" ")[3] + "\n"
        elif line.startswith("Type"):
            PutStr = line.split(" ")[1].replace(",", "") + " " + line.split(" ")[3]

            line = DumpFile.readline()
            while line != "\n":
                if not line:
                    break
                PutStr += line
                line = DumpFile.readline()

            PutStr += "\n\n"

        # print(PutStr);
        MakeFile.write(PutStr)

    DumpFile.close()
    MakeFile.close()

    # 간단한 디버그 용 코드.
    MakeFile = open('1G HexaDumpData', 'r')

    while True:
        Debug = MakeFile.readline()
        if not Debug:
            break

        if Debug.startswith("--- N0."):
            continue

        for Char in Debug:
            if (Char < '0' or '9' < Char) and (Char < 'A' or 'F' < Char) and Char != " " and Char != "\n" and (
                    Char < 'a' or 'f' < Char):
                print("Error!!!! : " + Char + "\n\n")

    MakeFile.close()


def Parsing_PIU_16SC_1G():
    MakeFile = open(HexDumpDataFileName_PIU_16SC_1G, 'r')

    Input = ""
    Count = 0

    Input2 = ""
    ResultData = []

    while True:
        line = MakeFile.readline()
        if not line:
            print(Input)
            Obj = _1G_MSG(Input)
            Count += 1
            Obj.Print()
            break

        if line.startswith("--- N0."):
            if Input == "":
                continue

            print(Input)
            Obj = _1G_MSG(Input)
            Count += 1
            Obj.Print()

            Input = ""
            continue

        Input += line

    MakeFile.close()

    print("End: " + str(Count))







def parse_data_to_dict(data):
    # 각 구조로 분리하여 딕셔너리로 저장
    parsed_daa = {
        "Dst" : data [:6 * 2],
        "Src" : data [6 * 2 : 12 * 2],
        "Len_Type" : data [12 * 2 : 14 * 2],
        "Subtype": data[14 * 2: 15 * 2],
        "Flags": data[15 * 2: 17 * 2],
        "Code": data[17 * 2: 18 * 2],
        "DataAndPad": data[18 * 2: ],
    }

    return parsed_daa


def Parsing_PIU_16SC_1G_2():
    MakeFile = open(HexDumpDataFileName_PIU_16SC_1G, 'r')

    Input = ""
    Count = 0
    ResultData = []


    while True:
        line = MakeFile.readline()

        if line.startswith("--- N0.") or not line:
            if Input == "":
                continue

            print(Input)
            data = Input.replace(" ","").replace("\n", "")
            print(data)
            Obj = parse_data_to_dict(data)
            ResultData.append(Obj)
            print(Obj)
            Count += 1

            if line.startswith("--- N0."):
                Input = ""
                continue

            if not line:
                break

        Input += line

    MakeFile.close()

    print(ResultData);
    print("End: " + str(Count))



def HostMsgParser(FileName: str):

    DumpToHexData_PIU_16SC_1G(FileName)
    Parsing_PIU_16SC_1G_2()





HostMsgParser('1G Dump')
