"""THIS IS ADITYA'S LIBRARY. YOU'LL FIND ALL SORTS OF FUNCTIONS HERE AND THEY ARE EXTREMELY EFFICIENT AND SHORT."""

"""-------------------------------------VERSION 0.21---------------------------------------------------"""

"""CHANGE LOG:
            V0.10--> Basic math functions, printing a tree and sorting
            V0.11-->Decimal to binary only in int format in one line
            V0.12-->Nth Fibonacci term in one line
            V0.13-->Changed binary conversion functions and more number system conversions
            V0.20-->Added data structures Stack and Queue
            V0.21-->Added one liner binay search function
            V0.22-->Added creating of immutable classes to pass by value and not by reference
"""

#For creating an immutable class
import inspect

#checking if a number is prime
prime_check = lambda x: True if not len([i for i in range(2,int(x**0.5)+1) if not x%i and x!=i]) else False

#returning the factorial of a number
factorial = lambda x: 1 if not x else x*factorial(x-1)

#returning the gcd/hcf of 2 numbers
hcf = gcd = lambda x,y: y if not x%y else gcd(y,x%y)

#returning the lcm of 2  numbers
lcm = lambda x,y: x*y/gcd(x,y)

#returning a list of n fibonacci numbers starting from a,b
def fibonacci(a,b,n,l=[]):
    if not n: return l
    l.append(a+b); return fibonacci(b,a+b,n-1,l) 

fib = lambda x: 1 if x <= 1 else fib(x-1) + fib(x-2)
# CALL IN THIS MANNER ([fib(i) for i in range(10)])

#returning the next prime after a number
next_prime = lambda x: x if prime_check(x) and x!=1 else [i for i in range(x+1,2*x+1) if prime_check(i)][0]

#printing a tree
def tree(h,w,a=0):
    for i in range(0,2*h,2):
        print(' '*(h-a)+'*'*i)
        a+=1
    for i in range(0,h):
        print(' '*(int(h-w/2)+2)+'*'*(int(w/2)))

#sorting a list using selection sort  
def cont(l,n): l.pop(l.index(temp:=min(l[n:len(l)]))); l.insert(n,temp);return list_sort(l,n+1)
list_sort = lambda l,n=0: l if n==len(l) else cont(l,n)

#Decimal to binary
d2b_float = lambda x,n,s='' : s if n==0 else d2b_float(2*x-int(2*x),n-1,s+str(int(2*x)))
d2b_int=lambda x,s='': s[::-1] if not x else d2b_int(x//2,s:=s+str(x%2))
d2b = lambda x,n=3: d2b_int(int(x))+"."+d2b_float((x-int(x)),n)

#Decimal to octal
d2o_int = lambda x,s='': s[::-1] if x==0 else d2o_int(x//8,s+str(x%8))
d2o_float = lambda x,n,s='' : s if n==0 else d2o_float(8*x-int(8*x),n-1,s+str(int(8*x)))
d2o = lambda x,n=3: d2o_int(int(x))+'.'+d2o_float((x-int(x)),n)

#Decimal to hexadecimal
hex_list=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
d2h_int = lambda x,s='': s[::-1] if x==0 else d2h_int(x//16,s+str(hex_list[x%16]))
d2h_float = lambda x,n,s='' : s if n==0 else d2h_float(16*x-int(16*x),n-1,s+str(hex_list[int(16*x)]))
d2h = lambda x,n=3: d2h_int(int(x))+'.'+d2h_float((x-int(x)),n)

#Stack data structure with basic methods
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self,i):
        self.items.append(i)
    
    def pop(self):
        return self.items.pop()
    
    def get_stack(self):
        return self.items
    
    def is_empty(self):
        return self.items == []
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None


#Queue data structure with basic methods
class Queue:
    items = []
    position = 0
    def __init__(self,maxLength):      
        self.maxLength = maxLength
    
    def enqueue(self,item):
        self.items.insert(self.position,item)
        self.position+=1
        self.position%=self.maxLength

    def dequeue(self):
        return self.items.pop(0) if not self.isEmpty() else None

    @staticmethod
    def isEmpty(self):
        return not len(self.items)
    
    def rear(self): 
        return self.items.pop(-1) if not self.isEmpty() else None


#Creating an immutable class for passing parameters by value
class Immutable(object):
    def __init__(self, x):
        self.x = x

    def __setattr__(self, *args):
        if inspect.stack()[1][3] == '__init__':
            object.__setattr__(self, *args)
        else:
            raise TypeError('Cannot modify immutable instance')

#binary_search of a sorted list    
bin_search = lambda arr,x: True if (len(arr)==1 and arr[0]==x) else False if (len(arr)==1 and arr[0]!=x) else bin_search(arr[len(arr)//2:],x) if x>=arr[len(arr)//2] else bin_search(arr[:len(arr)//2],x)
