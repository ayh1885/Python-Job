

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
    MakeFile = open(HexDumpDataFileName_PIU_16SC_1G, 'r')

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


def parse_data_to_dict(data):
    # 각 구조로 분리하여 딕셔너리로 저장
    parsed_data = {
        "Dst" : data [:6 * 2],
        "Src" : data [6 * 2 : 12 * 2],
        "Len_Type" : data [12 * 2 : 14 * 2],
        "Subtype": data[14 * 2: 15 * 2],
        "Flags": data[15 * 2: 17 * 2],
        "Code": data[17 * 2: 18 * 2],
        "DataAndPad": data[18 * 2: ],
    }

    return parsed_data


def Parsing_PIU_16SC_1G():
    MakeFile = open(HexDumpDataFileName_PIU_16SC_1G, 'r')

    Input = ""
    Count = 0
    ResultData = []

    OneLineData = []

    while True:
        line = MakeFile.readline()

        if line.startswith("--- N0.") or not line:
            if Input == "":
                continue

            print(Input)
            data = Input.replace(" ","").replace("\n", "")
            print(data)
            OneLineData.append(data)

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

    return OneLineData


def HostMsgParser(FileName: str):

    DumpToHexData_PIU_16SC_1G(FileName)
    Parsing_PIU_16SC_1G()









HostMsgParser('1G Dump')
