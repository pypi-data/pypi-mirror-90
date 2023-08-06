

def Log(message):
    with open("output.txt","a") as f:
        print(message)
        f.write(message)
        f.close()
        return
