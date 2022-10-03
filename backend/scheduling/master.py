for i in range(int(input("How many times would you like to run this?"))):
    exec(open("backend/scheduling/testgen.py").read())
    exec(open("backend/scheduling/scheduling.py").read())
