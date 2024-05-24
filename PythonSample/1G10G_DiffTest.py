from locale import str

HexDumpDataFileName_PIU_16SC_1G = '1G HexaDumpData'

def DebugLine(string : str):

    for Char in string:
        if (Char < '0' or '9' < Char) and (Char < 'A' or 'F' < Char) and Char != " " and Char != "\n" and (
                Char < 'a' or 'f' < Char):
            return False

    return True

def DumpToHexData_PIU_16SC_1G(FileName:str):

    DumpFile = open(FileName, 'r', encoding="UTF-8")
    MakeFile = open(HexDumpDataFileName_PIU_16SC_1G, 'w', encoding="UTF-8")

    Num = 1

    while True:
        line = DumpFile.readline()
        if not line:
            break
        # line.strip()

        PutStr = ""

        if line.startswith("D: "):
            MakeFile.write("--- N0." + str(Num) + " -------------------------------------------------\n\n")
            Num += 1
            try:
                PutStr = line.split(" ")[1] + " " + line.split(" ")[3] + " " + line.split(" ")[5].replace("[", "").replace(
                "]", "")
                if not DebugLine(PutStr):
                    print(PutStr)
                    input()
                    raise Exception


            except Exception as e:
                print("Abnormal Data in Dump!!!")
                print(line)
                MakeFile.write("// Error : " + line)
                continue

        elif line.startswith("SubType: "):
            PutStr = line.split(" ")[1] + " " + line.split(" ")[3] + "\n"

        elif line.startswith("Type"):
            try:
                PutStr = line.split(" ")[1].replace(",", "") + " " + line.split(" ")[3]
            except Exception as e:
                print("Abnormal Data in Dump!!!")
                MakeFile.write("// Error : " + line)
                continue

            else:
                line = DumpFile.readline()
                while line != "\n":
                    if not line:
                        break

                    if line.startswith("["):
                        break


                    PutStr += line
                    line = DumpFile.readline()

                PutStr += "\n\n"

        # print(PutStr)
        MakeFile.write(PutStr)

    DumpFile.close()
    MakeFile.close()

    # 간단한 디버그 용 코드.
    MakeFile = open('1G HexaDumpData', 'r', encoding="UTF-8")

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

        if line.startswith("//"):
            continue

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

    print(ResultData)
    print("End: " + str(Count))

    return OneLineData


def HostMsgParser(FileName: str):

    DumpToHexData_PIU_16SC_1G(FileName)
    return Parsing_PIU_16SC_1G()







####################################################################
####################################################################
####################################################################



def EMGRD_ONELINE():
    Dump1 = open("EMGRD", 'r')

    Online = []
    while True:
        line = Dump1.readline()
        if not line:
            break
        # line.strip()

        if line == "\n":
            continue
        str = line.replace(" ","").replace("\n","")
        print(str + "\n\n")
        Online.append(str)

    Dump1.close()
    return Online


def EONTMD_ONELINE():
    Online = []
    Dump2 = open("EONTMD", 'r')

    while True:
        line = Dump2.readline()
        if not line:
            break
        # line.strip()

        if line == "\n":
            continue

        str = line.replace(" ","").replace("\n","")
        print(str + "\n\n")
        Online.append(str)

    Dump2.close()
    return Online


####################################################################
####################################################################
####################################################################





HostMsgOneline = HostMsgParser('1G Dump')
EmgrdMsgOneline = EMGRD_ONELINE()
EontmdOneLine = EONTMD_ONELINE()



def Check_0050(list):
    print("startstart 0050")

    a = 0

    for data in list:
        a += 1
        ret = parse_data_to_dict(data)
        if ret.get("Flags") != "0050":
            print("///////////////////////////////////////////////////\nError\n")
            print(data)
            print (a)
            print("///////////////////////////////////////////////////\n")


# 1개 나옴.
Check_0050(HostMsgOneline)
Check_0050(EmgrdMsgOneline)
Check_0050(EontmdOneLine)

'''
def CheckRedunduncyInSameList(DataList : list):
    print("///////////////////////////\n//\tNew Check\n///////////////////////////\n")
    i = 0
    for Compare1 in DataList:
        i += 1
        for Compare2 in DataList[i:len(DataList)]:
            if Compare1 == Compare2:
                DataList.remove(Compare2)
                print(Compare1 + " == " + Compare2)
                print("delete!!!\n\n")
'''


# 같은 리스트에 있는 중복 데이터 제거.
def CheckRedunduncyInSameList(DataList : list):
    print("///////////////////////////\n//\tNew Check\n///////////////////////////\n")
    for Compare1 in list(DataList):  # Create a copy of the list for iteration
        if DataList.count(Compare1) > 1:  # If the element appears more than once
            DataList.remove(Compare1)  # Remove it from the original list
            print(Compare1 + " == " + Compare1)
            print("delete!!!\n\n")


print(len(HostMsgOneline))
CheckRedunduncyInSameList(HostMsgOneline)
print(len(HostMsgOneline))

'''
CheckRedunduncyInSameList(HostMsgOneline)
print(len(HostMsgOneline))
'''

print(len(EmgrdMsgOneline))
CheckRedunduncyInSameList(EmgrdMsgOneline)
print(len(EmgrdMsgOneline))


print(len(EontmdOneLine))
CheckRedunduncyInSameList(EontmdOneLine)
print(len(EontmdOneLine))



def CompareTwoList(Datalist1 : list, DataList2 : list):
    Match = 0
    for Comp1 in Datalist1:
        for Comp2 in DataList2:
            if Comp1 == Comp2:
                print(Comp1 + " == " + Comp2)
                Match += 1
    print("////////////////////////////////////////////")
    print("Match Test!!!" + str(Match) + "  :  ")
    print("////////////////////////////////////////////\n\n")



# 흠 .... 제일 의미 있는 1, 2번쨰가 다르네...
CompareTwoList(HostMsgOneline, EmgrdMsgOneline)
CompareTwoList(HostMsgOneline, EontmdOneLine)
CompareTwoList(EmgrdMsgOneline, EontmdOneLine)




# 이제 해야할 일 = leaf를 추출하자...   - 일단, 일반적인 형태의 모습...

def ExtractLeaf(OamData : dict, StoreDict : dict):
    OamDataAndPad = ""
    OamDataAndPad = OamData.get("DataAndPad")

    # 이것을 기준으로 Var에 대한 값을 가져갈 것이다.
    StrLen = len(OamDataAndPad)

    if StrLen < 4*2:
        return -1

    # OUI 3 Byte    + 추가사항 = 0xaaaaaa   = KT 이다.
    OUI = OamDataAndPad[ 0 : 3*2 ]
    print("OUI = " + OUI)

    # 1 Byte
    #해당 op 값을 기반으로 아래의 값이 매칭이 될 듯 하다. + OUI 에 대해서도 변ㄱㅇ
    Op = OamDataAndPad[ 3*2 : 4*2]
    print("Op =  " + Op)


    # 차후 op = 01인것도 해야 할 듯,,, + Op == 0인 Info 데이터도 있다.
    if (int(Op, 16) != 2) and (int(Op, 16) != 3) and (int(Op, 16) != 4):
        return -1





    ########################################################
    # 여기부터 Var영역이다. - 반복문으로 전환해야 한다.            #
    ########################################################
    '''
    # Branch 1바이트이다. - HEX 값인것을 인지 해야 한다.
    Branch = OamDataAndPad[ 4*2 : 5*2 ]

    # 이것도 고려를 해야 한다.
    if Branch == "07":
        print("0x07 is Attribute!!")

    # 위의 Branch가 07이면, 아래 2 Byte가 leaf이다.   // leaf가 아닌 경우도 있지만, 2바이트를 차지하는 것은 같다.
    leaf = OamDataAndPad[ 5*2 : 7*2 ]
    print("leaf : " + leaf)

    # 위가 1바이트 leaf라면은 여기는 Width 값이다.    // leaf가 아닌 경우에도 지금 length 값으로 width와 비슷한 역할을 한다.
    width = OamDataAndPad[ 7*2 : 8*2 ]
    print("width : " + width)

    # 현재는 일단 ... 이대로 놔두자.
    ParsedData = OamDataAndPad[ 8*2 : (8 + width)*2 ]
    '''


    WorkByte = 4

    while(True):
        if StrLen <= WorkByte*2:
            break

        LeafFlag = True

        # Branch 1바이트이다. - HEX 값인것을 인지 해야 한다.
        Branch = OamDataAndPad[WorkByte * 2: (WorkByte+1) * 2]
        print(Branch)
        WorkByte += 1



        # 아외에 추가적인 사항이 있다면은 기재를 해야한다.
        if Branch == "00":
            print("0x00 is End!!")
            break

        if Branch == "06":
            LeafFlag = False
            print("Not Leaf Data... ")



        # 위의 Branch가 07이면, 아래 2 Byte가 leaf이다.   // leaf가 아닌 경우도 있지만, 2바이트를 차지하는 것은 같다.
        leaf = OamDataAndPad[WorkByte * 2: (WorkByte+2) * 2]
        WorkByte += 2
        if LeafFlag:
            print("leaf : " + leaf)
            StoreDict[int(leaf, 16)] = int(Branch, 16)
            '''
            # 나중에 빼야 하는 코드 - 이상값을 찾기 위한 코드
            if int(leaf, 16) == 23691 or int(leaf, 16) == 15274:
                print(OamData)
                #input()
            '''
            if int(Branch, 16) == 7 and int(leaf, 16) == 21:
                print(OamData)
                #input()


        # 위가 1바이트 leaf라면은 여기는 Width 값이다.    // leaf가 아닌 경우에도 지금 length 값으로 width와 비슷한 역할을 한다.
        width = OamDataAndPad[WorkByte * 2: (WorkByte+1) * 2]
        WorkByte += 1
        print("width : " + width)


        # 현재는 일단 ... 이대로 놔두자.
        ParsedData = OamDataAndPad[WorkByte * 2: (WorkByte + int(width, 16)) * 2]
        WorkByte += int(width, 16)





HostMsgDict = dict()
for Data in HostMsgOneline:
    ExtractLeaf(parse_data_to_dict(Data), HostMsgDict)

#print(HostMsgSet)




EmgrdMsgDict = dict()
for Data in EmgrdMsgOneline:
    ExtractLeaf(parse_data_to_dict(Data), EmgrdMsgDict)

#print(EmgrdMsgSet)



EontmdMsgDict = dict()
for Data in EontmdOneLine:
    ExtractLeaf(parse_data_to_dict(Data), EontmdMsgDict)




def CompareDictionary(Target : dict, Comp : dict):
    RetDict = {}
    for key1, value1 in Target.items():
        Flag = True
        for key2, value2 in Comp.items():
            if key1 == key2 and value1 == value2:
                Flag = False
                break
        if Flag:
            RetDict[key1] = value1

    return dict(sorted(RetDict.items()))



HostDictRet1 = CompareDictionary(HostMsgDict, EmgrdMsgDict)
HostDictRet2 = CompareDictionary(HostMsgDict, EontmdMsgDict)



for key, value in HostDictRet1.items():
    print(f"{key}: {value}")

print()

for key, value in HostDictRet2.items():
    print(f"{key}: {value}")


print()
print()

EmgrdDictRet1 = CompareDictionary(EmgrdMsgDict, HostMsgDict)
EontmdDictRet1 = CompareDictionary(EontmdMsgDict, HostMsgDict)


for key, value in EmgrdDictRet1.items():
    print(f"{key}: {value}")

print()
for key, value in EontmdDictRet1.items():
    print(f"{key}: {value}")