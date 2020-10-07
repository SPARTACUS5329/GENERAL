import os
import time
for i in range(50):
    if i%2:
        print("*"*50)
    else:
        print("#"*50)
    time.sleep(1)
    if os.name=='nt':
        os.system('cls')
    elif os.name=='posix':
        os.system('clear')

