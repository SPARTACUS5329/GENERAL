print("\n")


try:
    import pyperclip
    pc = True
except:
    print('pyperclip not found.\nuse\npython -m pip install pyperclip')
    pc = False

def generate(x,y):
    t = ''
    n = 0
    for i in range(len(y)):
        n += (-1**i)*ord(y[i])
    n = abs(n)
    n /= 100 if n > 500 else 50 if n > 300 else 20
    for i in range(len(x)):
        m = abs(ord(x[i]) + int((-i**(i%2))*n))
        if (i == 0 or i == len(x)-1) and m == 32: m+=5
        while m < 32: m*=2
        t += chr(m)
    print('Password:',t)
    try:
        pyperclip.copy(t)
        print('Password copied to clipboard.')
    except:
        if pc: print('There was an error copying the password to clipboard.\nIf you are using linux try:\nsudo apt-get install xclip')
        else: print('Install pyperclip to automatically copy the passwords.')
while True:
    print()
    x = input('Pass phrase(type exit to exit): ')
    if x == 'exit': quit()
    if len(x) < 10: print('WARNING: Pass phrase isn\'t long enough.\nPasswords of less than 10 character length are easy to brute-force.')
    y = input('Service: ')
    generate(x,y)
