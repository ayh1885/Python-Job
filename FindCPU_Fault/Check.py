
CheckFile = open('9716 NS2_Warm_Booting_Test - 2024-06-26.txt', 'r', encoding="UTF-8")

CheckNum = 1
Count = 0;

while True:

    line = CheckFile.readline()
    if not line:
        break


    if line.startswith("DBG TEE-CORE:generic_boot_cpu_on_handler:372: cpu 1: a0 0x0"):
        if CheckNum != 1:
            raise Exception
        else:
            print(line)
            CheckNum += 1

    if line.startswith("DBG TEE-CORE:generic_boot_cpu_on_handler:372: cpu 2: a0 0x0"):
        if CheckNum != 2:
            raise Exception
        else:
            print(line)
            CheckNum += 1


    if line.startswith("DBG TEE-CORE:generic_boot_cpu_on_handler:372: cpu 3: a0 0x0"):
        if CheckNum != 3:
            raise Exception
        else:
            print(line)
            CheckNum -= 2


print("Success!!!!!!");