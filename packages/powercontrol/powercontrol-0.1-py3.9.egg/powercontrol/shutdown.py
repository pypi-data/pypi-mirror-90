import os

def shutdown(time=20):
    os.system("shutdown /t" + time)
