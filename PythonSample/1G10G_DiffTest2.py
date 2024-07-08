#from locale import str
from datetime import datetime

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
    count = 0

    while True:
        Debug = MakeFile.readline()
        if not Debug:
            break

        if Debug.startswith("--- N0."):
            count += 1
            continue

        for Char in Debug:
            if (Char < '0' or '9' < Char) and (Char < 'A' or 'F' < Char) and Char != " " and Char != "\n" and (
                    Char < 'a' or 'f' < Char):
                print("Error!!!! : " + Char + "\n\n")
                print("Check MSG Please!!!  Conut : " + str(count))
                #raise Exception

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

        "FullData": data,
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
            if data == "":
                continue
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
            print("///////////////////////////////////////////////////\nError")
            print(ret)
            print(a)
            print("///////////////////////////////////////////////////\n")


# 0개 나옴.
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
CheckList = []

# width 값을 기반으로 이상이 있는 값에 대해서 저장하는 저장소
ErrorAttributeWithWidth = {}
def ExtractLeaf(OamData : dict, StoreDict : dict, PonChipName: str):
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
    #if (int(Op, 16) != 2) and (int(Op, 16) != 3) and (int(Op, 16) != 4) and (int(Op, 16) != 1):
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


        # 위가 1바이트 leaf라면은 여기는 Width 값이다.    // leaf가 아닌 경우에도 지금 length 값으로 width와 비슷한 역할을 한다.
        width = OamDataAndPad[WorkByte * 2: (WorkByte+1) * 2]
        WorkByte += 1


        if int(width, 16) >= 128:

            if int(width, 16) > 128:
                if not PonChipName in ErrorAttributeWithWidth:
                    ErrorAttributeWithWidth[PonChipName] = {}
                if not width in ErrorAttributeWithWidth[PonChipName]:
                    ErrorAttributeWithWidth[PonChipName][width] = []

                PushList = []
                PushList.append(Op)
                PushList.append(Branch)
                PushList.append(leaf)
                PushList.append(OamData["FullData"])

                ErrorAttributeWithWidth[PonChipName][width].append(PushList)
                '''
                if int(leaf,16) == 249 :
                    print(OamData["FullData"])
                    input()
                '''
                '''
                if width == "9F":
                    print(OamData["FullData"])
                    input()
                '''


            width = "00"
            LeafFlag = False


        # 현재는 일단 ... 이대로 놔두자.
        ParsedData = OamDataAndPad[WorkByte * 2: (WorkByte + int(width, 16)) * 2]
        OldWorkByte = WorkByte
        WorkByte += int(width, 16)

        if LeafFlag:
            print("leaf : 0x" + leaf + " width : 0x" + width + " Data : " + ParsedData)
            print()
            # StoreDict[int(leaf, 16)] = int(Branch, 16)

            # 나중에 빼야 하는 코드 - 이상값을 찾기 위한 코드

            if int(Branch, 16) == 167:# and int(leaf, 16) == 184 :
                print("Op :" + str(int(Op, 16)) + " leaf : " + str(int(leaf, 16)) + " Width : " + str(int(width, 16)))
                print(OamData["FullData"]);
                #input()

            if int(leaf, 16) == 16:# and int(leaf, 16) == 184 :
                print("Op :" + str(int(Op, 16)) + " leaf : " + str(int(leaf, 16)) + " Width : " + str(int(width, 16)))
                print(OamData["FullData"]);
                #input()


            #key = str(int(Branch, 16)) + "-" + str(int(leaf, 16))
            key = str(int(Branch, 16)) + "-" + str(int(leaf, 16)) + " " + Op

            if not key in CheckList:
                StoreDict[key] = set()
                CheckList.append(key)

            if StrLen < WorkByte*2:
                ParsedData = "*" + ParsedData
                #print("strlen: " + str(StrLen) + " WorkByte : " + str(WorkByte*2) + " OldWorkByte: " + str(OldWorkByte*2) + " width : " + width)
                #print(OamData["FullData"]);
                #input()
            else :
                ParsedData = " " + ParsedData

            #ParsedData += "/" + OamData["FullData"]
            #StoreDict[key].append(ParsedData);
            StoreDict[key].add(ParsedData);






HostMsgDict = dict()
CheckList = []
for Data in HostMsgOneline:
    ExtractLeaf(parse_data_to_dict(Data), HostMsgDict, "Redstone")
for key, value in HostMsgDict.items():
    print(f"{key}: {value}")



print("\n\n")
EmgrdMsgDict = dict()
CheckList = []
for Data in EmgrdMsgOneline:
    ExtractLeaf(parse_data_to_dict(Data), EmgrdMsgDict, "Aspen(EMGRD)")
for key, value in EmgrdMsgDict.items():
    print(f"{key}: {value}")



print("\n\n")
EontmdMsgDict = dict()
CheckList = []
for Data in EontmdOneLine:
    ExtractLeaf(parse_data_to_dict(Data), EontmdMsgDict, "Aspen(EONTMD)")
for key, value in EontmdMsgDict.items():
    print(f"{key}: {value}")







BranchNameDict = {}
BranchLeafStringDict = {}
def BranchLeafStringData(BranchByte: str, BranchName: str, BranchFileName: str):

    BranchNameDict[BranchByte] = BranchName
    BranchLeafStringDict[BranchByte] = {}

    BranchFile = open(BranchFileName, "r", encoding="UTF-8")

    while True:
        line = BranchFile.readline()

        if line.startswith("'''"):
            line = BranchFile.readline()
            while not line.startswith("'''"):
                line = BranchFile.readline()
            continue


        if not line:
            break

        print(line)
        if line.startswith("*") or line.startswith("/"):
            continue

        if line == "\n":
            continue

        if BranchByte == "7":
            LeafAndDescript = line.split(",", 3)
            Name = str(int(LeafAndDescript[0].replace(" ", ""), 16))
            BranchLeafStringDict[BranchByte][Name] = []
            BranchLeafStringDict[BranchByte][Name].append(LeafAndDescript[1])
            BranchLeafStringDict[BranchByte][Name].append(LeafAndDescript[2])
            BranchLeafStringDict[BranchByte][Name].append(LeafAndDescript[3].replace("\n", ""))
        elif BranchByte == "9":
            LeafAndDescript = line.split(",", 2)
            Name = str(int(LeafAndDescript[0].replace(" ", ""), 16))
            BranchLeafStringDict[BranchByte][Name] = []
            BranchLeafStringDict[BranchByte][Name].append(LeafAndDescript[1])
            BranchLeafStringDict[BranchByte][Name].append(LeafAndDescript[2].replace("\n", ""))

    BranchFile.close()


BranchLeafStringData("7", "Attributes", "Branch7")
BranchLeafStringData("9", "Actions", "Branch9")












OpName = {
    "00": "[0x00]Info",
    "01": "[0x01]Get Request",
    "02": "[0x02]Get Response",
    "03": "[0x03]Set Request",
    "04": "[0x04]Set Response",
}



def CompareTwoDictData(Comp1 : dict, Comp2 : dict,
                       MakeFileName : str, Comp1Name :str, Comp2Name : str,
                       PrintSameValueFlag : bool,
                       ResetFlag : bool):
    DiffDicts = {
        "00": [],
        "01": [],
        "02": [],
        "03": [],
        "04": [],
    }
    SameDicts = {
        "00": [],
        "01": [],
        "02": [],
        "03": [],
        "04": [],
    }


    if ResetFlag:
        MakeFile = open(MakeFileName, 'w', encoding='UTF-8')
    else:
        MakeFile = open(MakeFileName, 'a+', encoding='UTF-8')



    DiffCount = 0
    SameCount = 0



    for TargetKey, TargetList in Comp1.items():

        for Data in TargetList:
            # Comp의 Value를 순횐한다.
            if TargetKey in Comp2:

                for CompValue in Comp2[TargetKey]:

                    inName = TargetKey.split(" ")
                    InputString = ""

                    InputString += ("[Branch-Leaf]:".center(17) + " " + inName[0])
                    BranchLeaf = inName[0].split("-")

                    if BranchLeaf[0] in BranchLeafStringDict:
                        FindDict = BranchLeafStringDict[BranchLeaf[0]]

                        if BranchLeaf[0] == "7":
                            print(BranchLeaf[1])
                            print(type(BranchLeaf[1]))

                            if BranchLeaf[1] in FindDict:

                                LeafName = FindDict[BranchLeaf[1]][0]
                                ReadOrWrite =  FindDict[BranchLeaf[1]][1]
                                Description = FindDict[BranchLeaf[1]][2]
                            else:
                                LeafName = "-"
                                ReadOrWrite = "-"
                                Description = "-"

                            InputString += (" [Branch :" + BranchNameDict[BranchLeaf[0]]+ ", ")
                            InputString += ("LeafName :" + LeafName + ", R/W :" + ReadOrWrite + "] - Description :" + Description)

                        elif BranchLeaf[0] == "9":
                            LeafName = FindDict[BranchLeaf[1]][0]
                            Description = FindDict[BranchLeaf[1]][1]
                            InputString += (" [Branch :" + BranchNameDict[BranchLeaf[0]] + ", ")
                            InputString += ("LeafName :" + LeafName + "] - Description :" + Description)

                    else:
                        if BranchLeaf[0] == "167":
                            InputString += " [데이터 부재]"
                        else:
                            InputString += " [~~~확인 필요~~~~]"

                    InputString += "\n"
                    InputString += ("[" + Comp1Name.center(15) + "]: " + Data + "\n")
                    InputString += ("[" + Comp2Name.center(15) + "]: " + CompValue + "\n\n")

                    if Data != CompValue:
                        DiffCount += 1
                        DiffDicts[inName[1]].append(InputString)
                    else:   # Data == CompValue
                        SameCount+= 1
                        SameDicts[inName[1]].append(InputString)

    # 현재 날짜와 시간을 가져옵니다.
    now = datetime.now()
    # 날짜와 시간을 문자열로 변환합니다.
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    MakeFile.write("////////////////////////////////////////////////////////////////////////////////\n")
    MakeFile.write("//\t\t Test : ["+ Comp1Name + "] and ["+ Comp2Name +"]\n")
    MakeFile.write("//\t\t Test Time : " + date_string + "\n")
    MakeFile.write("////////////////////////////////////////////////////////////////////////////////\n")

    MakeFile.write("Note: \n")
    MakeFile.write("\t1. (*) 표시는 Msg 규격보다 더 넘어가는 width에 대하여 표시했습니다. + [7-184 : Egress Shaping]에 대한 확인 필요.\n")
    MakeFile.write("\t2. Branch가 [6]Name Binding인 경우 leaf가 아니라 Object여서 해당 Branch는 제외했습니다.  \n")
    MakeFile.write("\t3. Op이 0인 Info메시지와 leaf에 value 값이 없는 Op [01]Get Request는 제외했습니다.\n")
    MakeFile.write("\t4. ~~~~ 확인 필요 ~~~~ 값은 나오면 안됩니다.\n")

    MakeFile.write("\n")
    MakeFile.write("################################################################\n")
    MakeFile.write("#\t\t\tTest Fail - Different Value [DiffCount:" +  str(DiffCount)  +"]\n")
    MakeFile.write("################################################################\n")

    for key, value in DiffDicts.items():
        if key == "00" or key == "01":
            MakeFile.write("[제외 : Note 참고]")
        MakeFile.write("----- " + OpName[key] + " ------\n\n")
        for InputString in value:
            MakeFile.write(InputString)
            MakeFile.flush()

    if PrintSameValueFlag:
        MakeFile.write("################################################################\n")
        MakeFile.write("#\t\t\tTest Ok - Same Value [SameCount:" +  str(SameCount)  +"]\n")
        MakeFile.write("################################################################\n")
        for key, value in SameDicts.items():
            if key == "00" or key == "01":
                MakeFile.write("[제외]")
            MakeFile.write("----- Op Code : " + OpName[key] + " ------\n\n")
            for InputString in value:
                print(InputString)
                MakeFile.write(InputString)
                MakeFile.flush()


    MakeFile.write("////////////////////////////////////////////////////////////////////////////////\n\n\n\n")
    MakeFile.close()



print("==============================================================")

PrintSameFlag = False
CompareTwoDictData(HostMsgDict, EmgrdMsgDict,
                   "RedStone, Aspen Diff Test.txt", "Redstone", "16SC(EMGRD)",
                   PrintSameFlag,
                   True)
CompareTwoDictData(HostMsgDict, EontmdMsgDict,
                   "RedStone, Aspen Diff Test.txt", "Redstone", "16SC(EONTMD)",
                    PrintSameFlag,
                   False)










WithErrorDict = {}
WidthErrorFile = open("WidthError", "r", encoding="UTF-8")



while True:
    line = WidthErrorFile.readline()


    if not line:
        break
    if line == "\n":
        continue
    SplitString = line.split(",")

    Key = SplitString[2].replace(" ", "").replace("\n", "")

    WithErrorDict[Key]= []
    WithErrorDict[Key].append(SplitString[0])
    WithErrorDict[Key].append(SplitString[1])

WidthErrorFile.close()




'''
                if not PonChipName in ErrorAttributeWithWidth:
                    ErrorAttributeWithWidth[PonChipName] = {}
                if not width in ErrorAttributeWithWidth[PonChipName]:
                    ErrorAttributeWithWidth[PonChipName][width] = []

                PushList = []
                PushList.append(Op)
                PushList.append(Branch)
                PushList.append(leaf)
                PushList.append(OamData["FullData"])

                ErrorAttributeWithWidth[PonChipName][width].append(PushList)
'''
print(type(ErrorAttributeWithWidth))


TempFile = open("RedStone, Aspen Diff Test.txt", "a+", encoding="UTF-8")

TempFile.write("////////////////////////////////////////////////////////////////////////////////\n")
TempFile.write("//\t\t Width Error Msg\n")
TempFile.write("////////////////////////////////////////////////////////////////////////////////\n")

TempFile.write("\nNote: \n")
TempFile.write("\t1. 작업 기준(wiki) : https://wiki.ubiquoss.com/download/attachments/110930728/EPON_ONUxG-PG302-R26X-R33X-RDS%20-%20BRCM%20OAM%20Extension.pdf?api=v2\n\t\t3.2.4 Broadcom(Tek) OAM message.pdf - page.28\n")
TempFile.write("\t2. Branch:0x07, Leaf:0x00B9(249)에 대한 내용이 PDF에 없습니다. 이와같은 데이터는 LeafName과 Description이 - 로 표시됩니다.\n")
TempFile.write("\t3. ~~~~ 확인 필요 ~~~~ 값은 나오면 안됩니다.\n")


for PonChipName, PonDict in ErrorAttributeWithWidth.items():

    InputString = "\n\n"
    InputString += "----------------------------------------------------\n"
    InputString += ("| PonChipName: " +  PonChipName + "\n")
    InputString += "----------------------------------------------------\n\n"

    for Width, OpBranchLeafFull_List in PonDict.items():
        if not Width in WithErrorDict:
            continue
        InputString += ("Error Width = 0x" + Width + " : " + WithErrorDict[Width][0] + " -" + WithErrorDict[Width][1] + "\n\n")
        print(type(OpBranchLeafFull_List[0]))
        for List in OpBranchLeafFull_List:

            InputString += ("\t OP :" + " [" + OpName[List[0]] + "]")

            if str(int(List[1], 16)) in BranchLeafStringDict:
                FindDict = BranchLeafStringDict[str(int(List[1], 16))]

                InputString += (", Branch : 0x" + List[1] + " [" + BranchNameDict[str(int(List[1], 16))] + "]")
                      # FindDict의 키 값으로 - leaf값에 대해서 HexString -> Int -> IntString로 변환한 값을 사용한다.
                if str(int(List[2],16)) in FindDict:

                    LeafName = FindDict[str(int(List[2],16))][0] + " "

                        # Branch에 대한 값을 판단해야 하므로
                    if str(int(List[1], 16)) == "7":
                        Descript = FindDict[str(int(List[2],16))][2]
                    elif str(int(List[1], 16)) == "9":
                        Descript = FindDict[str(int(List[2], 16))][1]
                    else:
                        Descript = "~~~~ 확인 필요 ~~~~"

                else:
                    LeafName = "-"
                    Descript = "-"
                InputString += (", Leaf : 0x" + List[2] + " [" + LeafName + "]")
                InputString += (" - Description :" + Descript + "\n")


            InputString += ("\t Full Data :" +  List[3] + '\n\n')

    TempFile.write(InputString)

TempFile.write("////////////////////////////////////////////////////////////////////////////////\n\n\n\n")

TempFile.close()





















###############################################################################################################
#       HexaOneLine로 변환된 DumpList의 요소를 집어넣으면 아래의 Dict 형태로 변환한다. - 아래 함수에서 사용
###############################################################################################################
def ParseDatatoDict(data):
    # 각 구조로 분리하여 딕셔너리로 저장
    parsed_data = {

        "Dst" : data [:6 * 2],                  # 6 Byte
        "Src" : data [6 * 2 : 12 * 2],          # 6 Byte
        "Len_Type" : data [12 * 2 : 14 * 2],    # 2 Byte
        "Subtype": data[14 * 2: 15 * 2],        # 1 Byte
        "Flags": data[15 * 2: 17 * 2],          # 2 Byte
        "Code": data[17 * 2: 18 * 2],           # 1 Byte
        "DataAndPad": data[18 * 2: ],           # Rest

        "FullData": data,                       # Hexa 형식 전체도 저장한다.
    }

    return parsed_data




###############################################################################################################
#       HexaOneLine로 변환된 DumpList를 OAM Header 부분대로 나누어서 Dict에 저장한 것을 List로 반환한다.
###############################################################################################################
def MakeListParsedDict(DumpHexaList : list):
    RetList = []

    for Data in DumpHexaList:
        DictData = ParseDatatoDict(Data)
        RetList.append(DictData)

    return RetList




def ExtractFromOAM_andPrintFile(OamDataDictList: list):
    OutFile = open("Temp Test Module.txt", "w", encoding="UTF-8");
    Count = 0



    for OamData in OamDataDictList:

        PutFullData = OamData["FullData"]
        if(PutFullData.startswith("//")):
            continue


        Count += 1
        InputString = "\n\n\n----- N0." + str(Count) + " -------------------------------------------------------------------------\n\n"




        InputString += "Full Data : " + PutFullData + "\n\n"

        InputString += "[Total : " + str(int(len(PutFullData)/2)) + "bytes ]\n\n"
        if  len(PutFullData) % 2 != 0:
            print("Length Error!!!")
            print(PutFullData)
            print(len(PutFullData))
            raise Exception

        for index in range(0, len(PutFullData)):
            InputString += PutFullData[index]

            if index % 2 != 0:
                InputString += " "
            if index % 16 == 15:
                InputString += "\n"

        InputString += "\n\n\n"




        '''
        "Dst" : data [:6 * 2],                  # 6 Byte
        "Src" : data [6 * 2 : 12 * 2],          # 6 Byte
        "Len_Type" : data [12 * 2 : 14 * 2],    # 2 Byte
        "Subtype": data[14 * 2: 15 * 2],        # 1 Byte
        "Flags": data[15 * 2: 17 * 2],          # 2 Byte
        "Code": data[17 * 2: 18 * 2],           # 1 Byte

        "DataAndPad": data[18 * 2: ],           # Rest
        '''

        InputString += "Dst: 0x" + OamData["Dst"] + "\n"
        InputString += "Src: 0x" + OamData["Src"] + "\n"
        InputString += "Len_Type: 0x" + OamData["Len_Type"] + "\n"
        InputString += "Subtype: 0x" + OamData["Subtype"] + "\n"
        InputString += "Flags: 0x" + OamData["Flags"] + "\n"
        InputString += "Code: 0x" + OamData["Code"] + "\n\n"



        OamDataAndPad = OamData["DataAndPad"]

        # 이것을 기준으로 Var에 대한 값을 가져갈 것이다.
        StrLen = len(OamDataAndPad)

        # 3Byte = OUI, 1Byte = Op
        if StrLen < 4 * 2:
            InputString += "!!!!!!!!!!!Length Error!!!!!!!\n\n"
            OutFile.write(InputString)
            continue

        # OUI 3 Byte
        OUI = OamDataAndPad[0: 3 * 2]
        # print("OUI = " + OUI)

        # 1 Byte
        # 해당 op 값을 기반으로 아래의 값이 매칭이 될 듯 하다. + OUI 에 대해서도 변경
        Op = OamDataAndPad[3 * 2: 4 * 2]
        # print("Op =  " + Op)

        InputString += "OUI : " + OUI + "\n"

        if Op in OpName:
            InputString += "Op : " + OpName[Op] + "\n\n"
        else:
            InputString += "Op : 0x" + Op + "\n\n"

        if int(Op, 16) == 0 or int(Op, 16) == 1:
            InputString += "Skip [00]Info and [01]Get Request \n\n"
            OutFile.write(InputString)
            continue

        # 현재 Op 코드가 0 (info), 1 () 인것은 제외하였다. - 이유 : Branch-Leaf-Width-Value에 대한 정보가 나오지 않는다.
        if (int(Op, 16) != 2) and (int(Op, 16) != 3) and (int(Op, 16) != 4):
            InputString += "!!! Please Check OAM Data and Python Code !!! \n\n"
            continue

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
        VariableCount = 1

        format_string = lambda input_string: ' '.join(
            [input_string[i:i + 2] for i in range(0, len(input_string), 2)])

        while (True):
            if StrLen <= WorkByte * 2:
                OutFile.write(InputString)
                break




            InputString += "VarNum : " + str(VariableCount) + "\n"
            VariableCount += 1


            # Branch 1바이트이다. - HEX 값인것을 인지 해야 한다.
            Branch = OamDataAndPad[WorkByte * 2: (WorkByte + 1) * 2]
            WorkByte += 1



            # 이 외에 추가적인 사항이 있다면은 기재를 해야한다.
            if Branch == "00":
                InputString += "\tBranch : 0x00 [0x00 is End!]\n"
                InputString += "\tvalue : " + format_string(OamDataAndPad[WorkByte * 2:]) + "\n\n"
                OutFile.write(InputString)
                break

            # if Branch == "06":

            # 위의 Branch가 07이면, 아래 2 Byte가 leaf이다.   // leaf가 아닌 경우도 있지만, 2바이트를 차지하는 것은 같다.
            leaf = OamDataAndPad[WorkByte * 2: (WorkByte + 2) * 2]
            WorkByte += 2


            InputString += "\t[Branch-Leaf] : " + str(int(Branch, 16)) + "-" + str(int(leaf, 16)) + "\t"


            #####################################################################################################

            if str(int(Branch, 16)) in BranchLeafStringDict:
                FindDict = BranchLeafStringDict[str(int(Branch, 16))]

                if Branch == "07":

                    if str(int(leaf, 16)) in FindDict:

                        LeafName = FindDict[str(int(leaf, 16))][0]
                        ReadOrWrite = FindDict[str(int(leaf, 16))][1]
                        Description = FindDict[str(int(leaf, 16))][2]
                    else:
                        LeafName = "-"
                        ReadOrWrite = "-"
                        Description = "-"

                    InputString += (" [Branch :" + BranchNameDict[str(int(Branch, 16))] + ", ")
                    InputString += (
                                "LeafName :" + LeafName + ", R/W :" + ReadOrWrite + "] - Description :" + Description)

                elif str(int(Branch, 16)) == "9":
                    LeafName = FindDict[str(int(leaf, 16))][0]
                    Description = FindDict[str(int(leaf, 16))][1]
                    InputString += (" [Branch :" + BranchNameDict[str(int(Branch, 16))] + ", ")
                    InputString += ("LeafName :" + LeafName + "] - Description :" + Description)

            else:
                if str(int(Branch, 16)) == "167":
                    InputString += " [데이터 부재 Case 1 - Branch == 167]"
                else:
                    InputString += " [데이터 부재 Case 2 - Data X]"

            InputString += "\n"


            ######################################################################################################






            InputString += "\tBranch : 0x" + Branch + "\n"
            InputString += "\tLeaf : 0x" + leaf + "\n"  # 여기에 인포가 들어가면 좋을 것이다.

            # 위가 1바이트 leaf라면은 여기는 Width 값이다.    // leaf가 아닌 경우에도 지금 length 값으로 width와 비슷한 역할을 한다.
            width = OamDataAndPad[WorkByte * 2: (WorkByte + 1) * 2]
            WorkByte += 1

            InputString += "\tWidth : 0x" + width + "  [" + str(int(width, 16)) + "]\n"

            if int(width, 16) >= 128:
                width = "00"


            Value = OamDataAndPad[WorkByte * 2: (WorkByte + int(width, 16)) * 2]


            WorkByte += int(width, 16)


            if int(width, 16) == 0:
                InputString += "\tValue : -NONE-\n\n"
            else:


                InputString += "\tValue : " + format_string(Value) + "\n\n"


    OutFile.close()



input()


DataList = Parsing_PIU_16SC_1G()
ExtractFromOAM_andPrintFile(MakeListParsedDict(DataList))

print(len(DataList))
