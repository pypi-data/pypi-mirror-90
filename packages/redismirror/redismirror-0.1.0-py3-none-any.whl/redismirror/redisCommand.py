
def setFunc(rLine, connection):
    line = rLine.split(" ", 5)
    keyName = line[4].strip('"')
    keyValue = line[5].strip('"')
    try:
        connection.set(keyName, keyValue)
        print(f"Key mirroed sucessfully | {keyName}")
    except Exception as e:
        print(f"Failed to set key | {keyName} | {e}")


def hsetFunc(rLine, connection):
    line = rLine.split(" ", 6)
    keyName = line[4].strip('"')
    hkeyName = line[5].strip('"')
    keyValue = str(line[6].strip('"')).lstrip('"\n')
    try:
        connection.hset(keyName, hkeyName, keyValue)
        print(f"Key mirroed sucessfully | {keyName}")
    except Exception as e:
        print(f"Failed to set key | {keyName} | {hkeyName} | {e} ")
