

def Log(message):
    with open("output.txt","w") as f:
        print(message)
        f.write(message)
        f.close()
        return
