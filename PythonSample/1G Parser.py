

# 1G parser Module



DumpFile = open('1G Dump', 'r');
MakeFile = open('1G HexaDumpData', 'w');


Num = 1;

while True:
    line = DumpFile.readline();
    if not line:
        break;
    #line.strip();

    PutStr = "";

    if line.startswith("D: "):
        MakeFile.write("--- N0." + str(Num) + " -------------------------------------------------\n\n")
        Num += 1;
        PutStr = line.split(" ")[1] + " " + line.split(" ")[3] + " " + line.split(" ")[5].replace("[", "").replace("]", "");
    elif line.startswith("SubType: "):
        PutStr = line.split(" ")[1] + " " + line.split(" ")[3] + "\n";
    elif line.startswith("Type"):
        PutStr = line.split(" ")[1].replace(",", "") + " " + line.split(" ")[3];

        line = DumpFile.readline();
        while line != "\n":
            if not line:
                break;
            PutStr += line;
            line = DumpFile.readline();

        PutStr += "\n\n";


    #print(PutStr);
    MakeFile.write(PutStr);


DumpFile.close();
MakeFile.close();



# 간단한 디버그 용 코드.
MakeFile = open('1G HexaDumpData', 'r');

while True:
    Debug = MakeFile.readline();
    if not Debug:
        break;

    if Debug.startswith("--- N0."):
        continue;

    for Char in Debug:
        if (Char < '0' or '9' < Char) and (Char < 'A' or 'F' < Char) and Char != " " and Char != "\n" and (
                Char < 'a' or 'f' < Char):
            print("Error!!!! : " + Char + "\n\n");


MakeFile.close();


