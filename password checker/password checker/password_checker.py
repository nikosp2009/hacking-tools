import random, time

password = input("Enter Password: ")

characters = '0123456789'
trypassword = ""
trypassswordtries = 0
timestart = time.time()

while True:
    trypassswordtries += 1

    for character in range(len(password)):
        trypassword = trypassword + characters[random.randint(0, 9)]
    
    timestop = time.time()
    timetotal = round(timestop - timestart, 1)

    if trypassword == password:
        print(f"{trypassswordtries} | valid | {trypassword} ({timetotal}s)")
        break
    else:
        print(f"{trypassswordtries} | Invalid | {trypassword}")

    trypassword = ""
