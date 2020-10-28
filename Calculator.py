class Stack:
    def __init__(self):
        self.items = []

    def push(self, i):
        self.items.append(i)

    def pop(self):
        return self.items.pop() if not self.is_empty() else "Stack Underflow"

    def get_stack(self):
        return self.items

    def is_empty(self):
        return self.items == []

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None

    def empty(self):
        self.items = []
        return None
    
    def length(self):
        return len(self.items)

class Expr:
    priorityOfOperations = {'+': 0, '-': 0, '*': 1, '/': 1}
    stack = Stack()
    postfix = ''
    cycle = 0

    def __init__(self, infix):
        self.infix = infix
        self.expression = self.infixToPostfixMain()

    def infixToPostfixMain(self):
        while self.cycle < len(self.infix):
            i = self.infix[self.cycle]
            result = self.infixToPostfix(i)
            if not result == "Operand":
                self.postfix += ' '
            if not result or result == "Operand":
                self.cycle += 1
        while self.postfix[0] == ' ':
            self.postfix = self.postfix[1:]
        while self.postfix[-1] == ' ':
            self.postfix = self.postfix[:-1]
        while '  ' in self.postfix:
            self.postfix = self.postfix.replace('  ', ' ')
        return self.postfix

    def infixToPostfix(self, i):
        top = self.stack.peek()
        if i == '(':
            self.stack.push('(')
            return False
        elif i in self.priorityOfOperations:
            if top == '(':
                self.stack.push(i)
                return False
            elif top in self.priorityOfOperations:
                if self.priorityOfOperations[i] <= self.priorityOfOperations[top]:
                    self.postfix += self.stack.pop()
                    return True
                else:
                    self.stack.push(i)
                    return False
        elif i == ')':
            while self.stack.peek() != '(':
                self.postfix += self.stack.pop()
            self.stack.pop()
            return False

        else:
            self.postfix += i
            return "Operand"

    def postfixCalculation(self):
        self.stack.empty()
        for j in range(len(self.expression)):
            i = self.expression[j]
            if i == ' ':
                continue

            if not i in self.priorityOfOperations:
                t = self.expression[j-1]
                if (not t in self.priorityOfOperations) and (t!= ' ') and j>0:
                    self.stack.push(self.stack.pop()+i)
                else:
                    self.stack.push(i)

            elif self.stack.length() == 1:
                return self.stack.peek()

            else:
                r = self.stack.pop()
                l = self.stack.pop()
                if i == '+':
                    self.stack.push(Plus(l, r).eval())
                elif i == '-':
                    self.stack.push(Minus(l, r).eval())
                elif i == '*':
                    self.stack.push(Times(l, r).eval())
                elif i == "/":
                    self.stack.push(Divide(l, r).eval())
                else:
                    raise "What the hell is happening?"
        return self.stack.peek()

class Divide(Expr):
    def __init__(self, l, r):
        self.l = float(l)
        self.r = float(r)

    def __str__(self):
        return f"({self.l}/{self.r})"

    def eval(self):
        return self.l/self.r

class Times(Expr):
    def __init__(self, l, r):
        self.l = float(l)
        self.r = float(r)

    def __str__(self):
        return f"({self.l}*{self.r})"

    def eval(self):
        return self.l*self.r

class Plus(Expr):
    def __init__(self, l, r):
        self.l = float(l)
        self.r = float(r)

    def __str__(self):
        return f"({self.l}+{self.r})"

    def eval(self):
        return self.l+self.r

class Minus(Expr):
    def __init__(self, l, r):
        self.l = float(l)
        self.r = float(r)

    def __str__(self):
        return f"({self.l}-{self.r})"

    def eval(self):
        return self.l-self.r

class Const(Expr):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def eval(self, exp):
        return self.val

class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def eval(self, exp):
        return exp[self.name]



expression = Expr(input("Enter the expression: "))
print(expression.expression)
print(expression.postfixCalculation())