for i in range(100):
    exec(open("backend/scheduling/testgen.py").read())
    exec(open("backend/scheduling/scheduling.py").read())