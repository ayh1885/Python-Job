def DumpToHexData_ONT(FileName:str):

    DumpFile = open(FileName, 'r', encoding="UTF-8")
    MakeFile = open("OutputFile", 'w', encoding="UTF-8")

    Num = 1

    bRecord_Data = true

    while True:

        line = DumpFile.readline()
        if not line:
            break

        # line.strip()

        PutStr = ""

        if line.startswith("#"):
            MakeFile.write("--- N0." + str(Num) + " -------------------------------------------------\n\n")
            Num += 1

            if bRecord_Data:
                PutStr += "Log MSG: " + line + "\n"







        MakeFile.write(PutStr)