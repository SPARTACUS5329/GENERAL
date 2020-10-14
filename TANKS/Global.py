try:
    import data,importlib
except:
    #("There was an ERROR loading game data!\nIf the error persists, consider re-installing the game from github.com/iamgroot9/iamgroot")
    quit()
try:
    from tkinter import *
except:
    from Tkinter import * # some systems use capital T
try:
    import winsound as ws
    found = True
except:
    import subprocess as sp
    found = False
from random import *

version = '7.0'

w1check = True
GameState, hit, HT, dmg, n, k = 40, [0], 'nil', [0], 0, 0
'''
# GameState takes multiple values based on which the colours and messages etc. changes would take place
# Purpose of each state is defined in the SetGame function as follows:
###-----# 1: Active/attack mode
###-----# 2: When the apponent takes damage
###-----# 10: During attack
###-----# 40: Just before start of a match, when tanks are acquiring their positions
###-----# 50: When tanks are moving in two-player mode
###-----# 80: Transition to next match
###-----# 100: End of Match
###-----# 0: In other screens
### GameStates are -ve for one player games and +ve for two player games
# hit is a result of attack and leads to damage
# dmg a.k.a DAMAGE is (hit - block)
# HT carries the attack name to be displayed
# n and k will be > 1 in case the attack has multiple beam hits involved
# n is the number of beams fired
# k is the number of blasts caused
'''

def DoNothing(*args): return # a useless function that would be the command of a disabled button or key press

def encode(pwd): # for encryption of passwords
    x = "0"
    for i in pwd:
        x += str(ord(i))
    return hex(int(x))

def sgm(x): return abs(x)//x # signum function, required for changing GameState with sign

def create_circle(x, y, r, canvas, f):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=f)

'---------------------------HOVER FUNCTIONS---------------------------'

def on_enter(button=0,attack=None,*args): # on mouse hover over attack buttons...
    global messagebox, initialmsg, initialcol
    
    if args:
        messagebox = args[0]  # in attack selection screen, messagebox is not available to Global so it is sent as an argument here
    if attack != None: # attack will be none when messagebox is not supposed to be updated, for ex. in main menu
        initialmsg = messagebox['text']
        initialcol = messagebox['fg']
        messagebox.config(fg = "#ff0",text = attack.comment if type(attack) != str else attack) # in ability selection screen, display message is sent as attack argument
    if button: button.config(fg="#ff0") # if button is used because in case of drift icons, there is no button to update, but only messagebox

def on_leave(button=0,col='#fff'):
    global messagebox
    try: # try statement is used because messagebox is not always there when this function is called, for ex. in main menu
        messagebox.configure(text = initialmsg, fg = initialcol)
    except: DoNothing()
    if button: button.config(fg=col)

'---------------------------ATTACK FUNTIONS---------------------------'

def accurate(x): # trying probability to see if attack works or not
    rtrn = random() * TankA.acc
    return True if rtrn > 1-x else False

def BotAtk():
    
    def maxDmg(): # this function helps selecting the attack that causes maximum damage, irrespective of accuracy
        newlist = []
        for i in w2.skillset:
            if i.dmg*i.boom > 0: newlist.append(i)
        a = max([i.dmg*i.boom for i in newlist])
        for i in newlist:
            if a == i.dmg*i.boom:
                #('take the bigger one!',end=" ")
                GetDamage(i)
                return
    def maxAcc(): # this function helps selecting a damaging attack with highest accuracy
        newlist = []
        #('most accurate damaging attack',end=": ")
        for i in w2.skillset:
            if i.dmg > 0: newlist.append(i)
        a = max([i.acc for i in newlist])
        for i in newlist:
            if a == i.acc:
                GetDamage(i)
                return

    if w2.name == "Overlord": # special case only for Overlord because other guys don't have Enrage
        if (w2.block < 55 or w2.atk < 55) or (w2.health - w1.health < -10 and w2.health > 20 and w2.block < 90 and w2.atk < 90):
            GetDamage(data.enrage)
            return
        elif (w1.health > 0.7 * w1.maxHealth) or (w2.health < 20 and w1.health > 20):
            GetDamage(choice([data.sectumsempra , data.reducto , data.expulso]))
            return
        elif w2.health >= 20 and w1.health <= 20:
            GetDamage(data.bombarda)
            return
        else:
            GetDamage(choice([data.sectumsempra , data.reducto , data.expulso , data.bombarda]))
            return
    
    if w1.health < 20 and w1.block - w1.maxBlock < 15:
        maxAcc()
        return
    if w2.health < 20:
        #('need healing, ',end='')
        if data.levicorpus in w2.skillset and (w1.health < 30 or data.reparo not in w2.skillset):
            GetDamage(data.levicorpus)
            return
        elif data.reparo in w2.skillset:
            if random() > 0.3:
                GetDamage(data.reparo)
                return
        else:
            maxDmg()
            return
            
    if (w2.health > 0.2*w2.maxHealth) and (w2.maxBlock - w2.block > 15) and (data.protego in w2.skillset):
        #(f'my defences are low! {w2.maxBlock} | {w2.block}',end=": ")
        GetDamage(data.protego)
        return
    if w1.block - w1.maxBlock > 15:
        if data.dissendium in w2.skillset and w1.health > 20 and w2.health > 20:
            #(f'playing smart huh? {w1.maxBlock} | {w1.block}',end=": ")
            GetDamage(data.dissendium)
            return
        else:
            maxDmg()
            return
            
    if w2.health > 0.7*w2.maxHealth and (data.levicorpus in w2.skillset or data.reparo in w2.skillset):
        newlist = []
        for i in w2.skillset:
            if i != data.levicorpus and i != data.reparo: newlist.append(i)
        #('healing not needed...',end=" ")
        GetDamage(choice(newlist))
        return
    
    #('random',end=": ")
    GetDamage(choice([w2.a1 , w2.a2 , w2.a3 , w2.a4 , w2.a5]))       

def GetDamage(x): # called when the player attacks
    global hit, TankA, TankB, dmg, HT, n
    n += 1 # beam index of attack
    HT = x # attack object
    if TankA.pImmune: TankA.pImmune -= 1
    if TankA.iImmune: TankA.iImmune -= 1
    if accurate(x.acc):
        hit.append((TankA.atk * x.dmg)/TankB.block)
        if HT.type != 'A': hit.append(-1) # in case of non-damaging abilities
        if HT.label == 'PetrificusTotalus':
            TankB.petrified = 2
            TankB.pImmune = 3
        elif HT.label == 'Impeio':
            TankB.imperius = 2
            TankB.iImmune = 3
        elif HT.label == 'LumosMaxima':
            TankB.acc -= 0.1
        if TankB.block <= 1: TankB.block = 1
    else: hit.append(0) # attack failed
    if hit[-1] > 0: dmg.append(int(hit[-1]*uniform(0.8,1.2)))
    else: dmg.append(0)
    #(HT.label)
    ChangeGameState() # switching to TRANSITION mode

'---------------------------CLASSES---------------------------'

class Tank:
    
    def __init__(self,player):
        if type(player) == data.Player:
            self.name = player.name
            self.health = self.maxHealth = player.maxHealth
            self.atk = self.maxAtk = player.maxAtk
            self.block = self.maxBlock = player.maxBlock
            self.level = player.level
            self.a1 = player.a1
            self.a2 = player.a2
            self.a3 = player.a3
            self.a4 = player.a4
            self.a5 = player.a5
            self.colour = player.colour
        else: # for two player mode
            self.name = player
            self.health = self.maxHealth = 100
            self.atk = 20
            self.block = 20
            self.level = 1
            self.a1 = data.stupefy
            self.a2 = data.confringo
            self.a3 = data.reducto
            self.a4 = data.bombarda
            self.a5 = data.incendio
            self.colour = "#00f"
        self.imperius = self.iImmune = self.petrified = self.pImmune = self.poison = 0
        self.acc = 1
        global w1check,w1,w2,TankA,TankB
        if GameState > 0:
            if w1check: # player 1 attacks first
                w1check = False
                w1 = TankB = self
            else: w2 = TankA = self
        elif GameState < 0:
            if w1check: # boss attacks first
                w1check = False
                w1 = TankA = self
            else: w2 = TankB = self
        else: w1 = self # when chosing tank colour
        # w1 declaration is important because tank graphics are created based on it

    def blockdrift(self,x=0): # when player's defence is buffed/nerfed
        self.block += x
        k = self.block - self.maxBlock
        if k<=(-self.maxBlock):
            self.block=0.1
        if k==0: # when block it is same as initial
            canvas73.itemconfig(self.blocklabel,fill="#000")
            canvas73.tag_bind("blocklabel",'<Enter>',DoNothing)
            canvas73.tag_bind("blocklabel",'<Leave>',DoNothing)
        else: # when block is lesser/greater than initial block
            canvas73.itemconfig(self.blocklabel,fill="#1f0" if k>0 else "#f00")
            k = str(k) if k<0 else '+'+str(k)
            canvas73.tag_bind("blocklabel",'<Enter>',lambda x: on_enter(0,f"Defence {k}"))
            canvas73.tag_bind("blocklabel",'<Leave>',lambda x: on_leave())
    def atkdrift(self,x=0):
        self.atk += x
        k = self.atk - self.maxAtk
        if k==0:
            canvas73.itemconfig(self.atklabel,fill="#000")
            canvas73.tag_bind("atklabel",'<Enter>',DoNothing)
            canvas73.tag_bind("atklabel",'<Leave>',DoNothing)
        else:
            canvas73.itemconfig(self.atklabel,fill="#1f0" if k>0 else "#f00")
            k = str(k) if k<0 else '+'+str(k)
            canvas73.tag_bind("atklabel",'<Enter>',lambda x: on_enter(0,f"Attack {k}"))
            canvas73.tag_bind("atklabel",'<Leave>',lambda x: on_leave())
        
    def __str__(self): # This magic method makes the object return its name when called in as a string
        return self.name # i.e. You just have to write down the 'object' instead of 'object.name' to add it's name to strings

    @property # this means self.hcolour is a property just like self.health and self.name and not a method self.hcolour()
    def hcolour(self): # it is created as a method property because it is dependent on health and is to be reassigned whenever health changes
        if self.health > self.maxHealth*0.7: return '#1f0'
        elif self.health > self.maxHealth*0.6: return '#5f0'
        elif self.health > self.maxHealth*0.5: return '#7f0'
        elif self.health > self.maxHealth*0.4: return '#bf0'
        elif self.health > self.maxHealth*0.3: return '#fd0'
        elif self.health > self.maxHealth*0.2: return '#f80'
        else: return '#f00'
        
    @property
    def skillset(self):
        return [self.a1 , self.a2 , self.a3 , self.a4 , self.a5]

    def tank(self,master,*c): # Tank graphics
        if c: self.colour = c
        y = int(master['height'])
        if w1==self:
            self.base=master.create_rectangle(60,y-100 , 110,y-51,fill=self.colour,outline=self.colour)
            self.top=master.create_rectangle(90,y-160 , 100,y-100,fill=self.colour,outline=self.colour)
            if self.level >= 10: # from level 10 onward, the turret is modified
                self.turret=master.create_polygon([100,y-140 , 104,y-140 , 104,y-144 , 108,y-144 , 108,y-140 , 112,y-140 , 112,y-144 , 116,y-144 , 116,y-140 , 120,y-160 , 120,y-144 , 124,y-144 , 124,y-140 , 128,y-140 , 128,y-144 , 132,y-144 , 132,y-140 , 136,y-140 , 136,y-144 , 140,y-144 , 140,y-140 , 150,y-140 , 150,y-130 , 140,y-130 , 140,y-126 , 136,y-126 , 136,y-130 , 132,y-130 , 132,y-126 , 130,y-126 , 128,y-130 , 124,y-130 , 124,y-126 , 120,y-126 , 120,y-130 , 100,y-130 , 100,y-140,],fill=self.colour)
            else:
                self.turret=master.create_rectangle(100,y-140,150,y-130,fill=self.colour,outline=self.colour)
            # second turret unlocks at level 15
            if self.level >= 15: self.turret2=master.create_rectangle(100,y-160 , 150,y-150,fill=self.colour,outline=self.colour)
            self.front=master.create_polygon([110,y-100 , 110,y-50 , 150,y-50 , 110,y-100],fill=self.colour)
            self.behind_upper=master.create_polygon([10,y-50 , 60,y-200 , 110,y-200 , 110,y-180 , 80,y-180 , 80,y-100 , 10,y-50],fill=self.colour)
            self.behind=master.create_polygon([60,y-100 , 60,y-50 , 10,y-50 , 60,y-100],fill=self.colour)
        else:
            x = int(master['width'])
            self.base=master.create_rectangle(x-60,y-100 , x-110,y-51,fill=self.colour,outline=self.colour)
            self.top=master.create_rectangle(x-90,y-160 , x-100,y-100,fill=self.colour,outline=self.colour)
            if self.level >= 10:
                self.turret=master.create_polygon([x-100,y-140 , x-104,y-140 , x-104,y-144 , x-108,y-144 , x-108,y-140 , x-112,y-140 , x-112,y-144 , x-116,y-144 , x-116,y-140 , x-120,y-160 , x-120,y-144 , x-124,y-144 , x-124,y-140 , x-128,y-140 , x-128,y-144 , x-132,y-144 , x-132,y-140 , x-136,y-140 , x-136,y-144 , x-140,y-144 , x-140,y-140 , x-150,y-140 , x-150,y-130 , x-140,y-130 , x-140,y-126 , x-136,y-126 , x-136,y-130 , x-132,y-130 , x-132,y-126 , x-130,y-126 , x-128,y-130 , x-124,y-130 , x-124,y-126 , x-120,y-126 , x-120,y-130 , x-100,y-130 , x-100,y-140,],fill=self.colour)
            else:
                self.turret=master.create_rectangle(x-100,y-140 , x-150,y-130,fill=self.colour,outline=self.colour)
            if self.level >= 15: self.turret2=master.create_rectangle(x-100,y-160 , x-150,y-150,fill=self.colour,outline=self.colour)
            self.front=master.create_polygon([x-110,y-100 , x-110,y-50 , x-150,y-50 , x-110,y-100],fill=self.colour)
            self.behind_upper=master.create_polygon([x-10,y-50 , x-60,y-200 , x-110,y-200 , x-110,y-180 , x-80,y-180 , x-80,y-100 , x-10,y-50],fill=self.colour)
            self.behind=master.create_polygon([x-60,y-100 , x-60,y-50 , x-10,y-50 , x-60,y-100],fill=self.colour)
        self.nextTurret = self.turret
        self.previousTurret = self.turret2 if self.level >= 15 else self.turret
        if GameState == 50: # the tanks will be shifted to outside of the screen before the match starts, they will start moving to acquire their positions from here
            x = -400 if self == w1 else 400
            master.move(self.base,x,0)
            master.move(self.top,x,0)
            master.move(self.turret,x,0)
            master.move(self.behind,x,0)
            master.move(self.front,x,0)
            master.move(self.behind_upper,x,0)
            try: master.move(self.turret2,x,0)
            except: DoNothing()
         
    def move(self,a): # make the tanks move
        if a == 0: return
        x = -1 if self == w2 else 1
        canvas73.move(self.base,x,0)
        canvas73.move(self.top,x,0)
        canvas73.move(self.turret,x,0)
        canvas73.move(self.behind,x,0)
        canvas73.move(self.front,x,0)
        canvas73.move(self.behind_upper,x,0)
        try: canvas73.move(self.turret2,x,0)
        except: DoNothing()
        canvas73.after(5,lambda: self.move(a-1))
        
    def lose(self): # destroy the tank
        x = -1 if self == w1 else 1
        canvas73.move(self.base,x,0)
        canvas73.move(self.top,0,-3)
        canvas73.move(self.turret,-7*x,-5)
        try: canvas73.move(self.turret2,-6*x,-5)
        except: DoNothing()
        canvas73.move(self.behind,x*2,-3.5)
        canvas73.move(self.front,-10*x,-1)
        canvas73.move(self.shield,-3*x,-4)
        canvas73.move(self.behind_upper,2*x,0)
        canvas73.after(2,self.lose)
        
    def Labels(self,canvas2x,frame,col):
        self.namelabel = Label(frame, text = self.name, bg = '#222', fg = '#fff', width = 70)
        self.healthlabel = Label(frame, bg = '#222', width = 70)
        self.levellabel = Label(frame, bg = '#222', width = 70, fg = '#fff', text=f'Level: {self.level}')
        self.namelabel.grid(row=1,column=col)
        self.healthlabel.grid(row=2,column=col)
        self.levellabel.grid(row=3,column=col)
        if self == w1:
            self.healthbar = canvas2x.create_rectangle(0,0 , 450,14 , fill = self.hcolour)
        else:
            self.healthbar = canvas2x.create_rectangle(550,0 , 1000,14 , fill = self.hcolour)
        x = 50 if self==w1 else 750
        self.blocklabel = canvas73.create_rectangle(x,0 , x+20,20 , fill='#000',tags="blocklabel")
        canvas73.create_text(x+10,10,fill="#000",text="B",tags="blocklabel")
        x+=20
        self.atklabel = canvas73.create_rectangle(x,0 , x+20,20 , fill='#000',tags="atklabel")
        canvas73.create_text(x+10,10,fill="#000",text="D",tags="atklabel")
        x+=20
        self.acclabel = canvas73.create_rectangle(x,0 , x+20,20 , fill='#000',tags="acclabel")
        canvas73.create_text(x+10,10,fill="#000",text="A",tags="acclabel")
        x+=20
        self.implabel = canvas73.create_rectangle(x,0 , x+20,20 , fill='#000',tags="implabel")
        canvas73.create_text(x+10,10,fill="#000",text="I",tags="implabel")
        x+=20
        self.petlabel = canvas73.create_rectangle(x,0 , x+20,20 , fill='#000',tags="petlabel")
        canvas73.create_text(x+10,10,fill="#000",text="P",tags="petlabel")
        
    def setActive(self):
        self.namelabel.config(bg = '#000', fg = '#10ff00')
        self.healthlabel.config(bg = '#000', fg = self.hcolour, text = self.health)
        self.levellabel.config(bg = '#000')
        try:canvas73.delete(self.shield)
        except:DoNothing()
        
    def setInactive(self):
        self.namelabel.config(bg = '#222', fg = '#fff')
        self.healthlabel.config(bg = '#222', fg = self.hcolour, text = self.health)
        self.levellabel.config(bg = '#222')
        y = int(canvas73['height'])
        if self==w1:
            self.shield=canvas73.create_polygon([110,y-200 , 110,y-180 , 160,y-180 , 160,y-100 , 180,y-100 , 220,y-150 , 180,y-200 , 110,y-200],fill=self.colour)
        elif self==w2:
            x = int(canvas73['width'])
            self.shield=canvas73.create_polygon([x-110,y-200 , x-110,y-180 , x-160,y-180 , x-160,y-100 , x-180,y-100 , x-220,y-150 , x-180,y-200 , x-110,y-200],fill=self.colour)

    def takeDamage(self,k=1,w=0): # causes changes in player's health
        x = -1 if self == w1 else 1
        x*=k # k is +ve for damage and -ve for heal
        fraction = 450/self.maxHealth # the distance the health bar would move for 1 health loss, since 450 is max length of health bar
        self.health -= 1*k
        if self.health < 0:
            self.health = 0
            return
        if self.health > self.maxHealth:
            self.health = self.maxHealth
            return
        self.healthlabel.config(text=self.health)
        canvas2x.move(self.healthbar,x*fraction,0)
        canvas2x.itemconfig(self.healthbar,fill=self.hcolour)
        if w>1: canvas73.after(10,lambda: self.takeDamage(k,w-1))

class beam:
    def __init__(self):
        x, y = int(canvas73['width']), int(canvas73['height'])
        if TankA == w1:
            if TankA.nextTurret == TankA.turret: self.laser = canvas73.create_rectangle(120,y-130 , 170,y-140, fill = HT.colour)
            else: self.laser=canvas73.create_rectangle(120,y-150 , 170,y-160,fill=HT.colour)                
            self.x = 5
        else:
            if TankA.nextTurret == TankA.turret: self.laser = canvas73.create_rectangle(x-170,y-130 , x-120,y-140, fill = HT.colour)
            else: self.laser=canvas73.create_rectangle(x-120,y-150 , x-170,y-160,fill=HT.colour)
            self.x = -5
        self.a = 0
        self.n = n
        self.repeat = 140//HT.boom
        if self.repeat < 25: self.repeat = 25
        self.move()
    def move(self):
        if self.a == self.repeat:
            TankA.nextTurret, TankA.previousTurret = TankA.previousTurret, TankA.nextTurret
            if self.n < HT.boom:
                #(f'laser no ={self.n}')
                ChangeGameState(sgm(GameState))
                GetDamage(HT)
        if (self.a == 120 and dmg[self.n] == 0) or (self.a == 140):
            #(f'blasting laser {self.n}')
            ChangeGameState(2*sgm(GameState))
            blast(self)
            SetGame()
            if self.a == 140:
                if found: ws.PlaySound('damage.wav', ws.SND_FILENAME | ws.SND_ASYNC)
                else: sp.Popen(['afplay','damage.wav'])
            else:
                if found: ws.PlaySound('block.wav', ws.SND_FILENAME | ws.SND_ASYNC)
                else: sp.Popen(['afplay','block.wav'])
            #(f'done blasting laser {self.n}')
            return
        if self.a < 20:
            canvas73.move(TankA.nextTurret, -self.x/4, 0)#recoil
        elif self.a < 40:
            canvas73.move(TankA.nextTurret, self.x/4, 0)
        self.a += 1
        canvas73.move(self.laser, self.x, 0)
        canvas73.after(5, self.move)

class blast:
    def __init__(self,laser):
        global k
        k = laser.n # laser number
        self.dmg = dmg[k]
        self.up = 0
        if HT.label == 'Levicorpus' and hit[-1]>0: self.up=10
        elif HT.label == 'SalvioHexia' and hit[-1]>0: self.up=self.dmg
        self.r = 1
        x1,y1,x2,y2 = canvas73.coords(laser.laser)
        self.x, self.y = (x1+x2)/2, (y1+y2)/2
        self.circle = create_circle(self.x,self.y,self.r,canvas73,"#ff0")
        canvas73.delete(laser.laser)
        self.move()
    def move(self):
        global k, HT, dmg, hit, n
        canvas73.delete(self.circle)
        self.r += 1
        if self.r >= 30:
            if (self.dmg == 0) or (TankB.health == 0):
                if type(HT) != str:
                    if k == HT.boom: # GameState will be changed here allowing the opponent to play
                        #(f'k={k} | HT.boom={HT.boom}')
                        k = n = 0
                        dmg, hit, HT = [0], [0], 'nil'
                        #(f'GameState: {GameState}')
                        ChangeGameState()
                    else: # in case more beams are are to be shot
                        #(f'k={k} | HT.boom={HT.boom}')
                        #('ok hai')
                        ChangeGameState(10*sgm(GameState))
                        #(GameState)
                return
            self.r = 10
        else:
            self.circle = create_circle(self.x,self.y,self.r,canvas73,"#ff0")
        if self.dmg > 0:
            TankB.takeDamage(+1)
            self.dmg -= 1
        if self.up > 0:
            TankA.takeDamage(-1)
            self.up -= 1
        canvas73.after(10, self.move)

"---------------------------STATE FUNCTIONS---------------------------"

def SetGame(*args): # this function will make display changes acc to GameState
    global TankA,TankB,dmg,hit,messagebox,HT,a1,a2,a3,canvas2x,w1,load,game_window,n,k
    #(f'GameState: {GameState}')
    
    if args:
        load = args[1]
        game_window = args[0]

    if abs(GameState) == 1:
        if TankA.poison:
            TankA.takeDamage(1,10)
            TankA.poison -= 1
            x = randint(175,225)
            y = randint(275,325)
            x = x if TankA == w1 else 1000-x
            l1 = canvas73.create_text(x,y,fill="#fc0",text='-10',font=(None,25))
            canvas73.after(800,lambda: canvas73.delete(l1))
        
        TankA, TankB = TankB, TankA
        if TankB.health == 0:
            ChangeGameState(2*sgm(GameState))
            ChangeGameState()
        TankA.setActive()
        TankB.setInactive()
        if TankA.imperius:
            GetDamage(choice(TankA.skillset))
            return

        if (GameState == 1) or (TankA == w1): # ATTACK mode
            a1.config(bg = '#000', cursor = 'hand2', text = TankA.a1.label) # Enabling attack buttons
            a2.config(bg = '#000', cursor = 'hand2', text = TankA.a2.label)
            a3.config(bg = '#000', cursor = 'hand2', text = TankA.a3.label)
            a4.config(bg = '#000', cursor = 'hand2', text = TankA.a4.label)
            a5.config(bg = '#000', cursor = 'hand2', text = TankA.a5.label)
            a1.bind("<Enter>",lambda x: on_enter(a1,TankA.a1))
            a1.bind("<Leave>",lambda x: on_leave(a1))
            a2.bind("<Enter>",lambda x: on_enter(a2,TankA.a2))
            a2.bind("<Leave>",lambda x: on_leave(a2))
            a3.bind("<Enter>",lambda x: on_enter(a3,TankA.a3))
            a3.bind("<Leave>",lambda x: on_leave(a3))
            a4.bind("<Enter>",lambda x: on_enter(a4,TankA.a4))
            a4.bind("<Leave>",lambda x: on_leave(a4))
            a5.bind("<Enter>",lambda x: on_enter(a5,TankA.a5))
            a5.bind("<Leave>",lambda x: on_leave(a5))
            a1.bind("<Button-1>",lambda x: GetDamage(TankA.a1))
            a2.bind("<Button-1>",lambda x: GetDamage(TankA.a2))
            a3.bind("<Button-1>",lambda x: GetDamage(TankA.a3))
            a4.bind("<Button-1>",lambda x: GetDamage(TankA.a4))
            a5.bind("<Button-1>",lambda x: GetDamage(TankA.a5))
            messagebox.config(text = f'It\'s {TankA}\'s turn to attack.' if GameState == 1 else 'It\'s your turn to attack.')
        else:
            canvas73.after(randint(1500,3000),BotAtk)
            messagebox.config(text = 'Waiting for the opponent to move...')

    elif abs(GameState) > 5:
        a1.config(bg = 'grey', fg = '#fff', cursor = 'arrow') # disabling attack buttons
        a2.config(bg = 'grey', fg = '#fff', cursor = 'arrow') # ChangeGameState will switch the game back to attack mode
        a3.config(bg = 'grey', fg = '#fff', cursor = 'arrow')
        a4.config(bg = 'grey', fg = '#fff', cursor = 'arrow')
        a5.config(bg = 'grey', fg = '#fff', cursor = 'arrow')
        a1.bind("<Enter>",DoNothing)
        a1.bind("<Leave>",DoNothing)
        a2.bind("<Enter>",DoNothing)
        a2.bind("<Leave>",DoNothing)
        a3.bind("<Enter>",DoNothing)
        a3.bind("<Leave>",DoNothing)
        a4.bind("<Enter>",DoNothing)
        a4.bind("<Leave>",DoNothing)
        a5.bind("<Enter>",DoNothing)
        a5.bind("<Leave>",DoNothing)
        a1.bind("<Button-1>",DoNothing)
        a2.bind("<Button-1>",DoNothing)
        a3.bind("<Button-1>",DoNothing)
        a4.bind("<Button-1>",DoNothing)
        a5.bind("<Button-1>",DoNothing)
        if abs(GameState) == 10:
            messagebox.config(text = f'{TankA} uses {HT}.', fg = "#fff")
            if HT.type=='A':
                beam()
                if found: ws.PlaySound('Shot.wav', ws.SND_FILENAME | ws.SND_ASYNC)
                else: sp.Popen(['afplay','Shot.wav'])
            elif HT.type=='N':
                canvas73.after(1000,ChangeGameState)
                if found: ws.PlaySound('nerf.wav', ws.SND_FILENAME | ws.SND_ASYNC)
                else: sp.Popen(['afplay','nerf.wav'])
            elif HT.type=='B':
                canvas73.after(1000,ChangeGameState)
                if found: ws.PlaySound('buff.wav', ws.SND_FILENAME | ws.SND_ASYNC)
                else: sp.Popen(['afplay','buff.wav'])
            elif HT.type=='H':
                canvas73.after(1000,ChangeGameState)
                if found: ws.PlaySound('heal.wav', ws.SND_FILENAME | ws.SND_ASYNC)
                else: sp.Popen(['afplay','heal.wav'])
            elif HT.type=='C':
                canvas73.after(1000,ChangeGameState)
                if found: ws.PlaySound('curse.wav', ws.SND_FILENAME | ws.SND_ASYNC)
                else: sp.Popen(['afplay','curse.wav'])

    elif GameState == 2 or GameState == -2:
        x = randint(175,225)
        y = randint(275,325)
        x = x if TankB == w1 else 1000-x
        if dmg[k]>0: l1 = canvas73.create_text(x,y,fill="#ff0",text=f'-{dmg[k]}',font=(None,25))
        elif HT.type=='A': l1 = canvas73.create_text(x,y,fill="#0ff",text='Attack Blocked!',font=(None,20))
        elif HT.label=='Protego':
            if hit[-1] == -1: TankA.blockdrift(+10)
            l1 = canvas73.create_text(1000-x,y,fill="#0f0",text='Defence +10' if hit[-1] == -1 else 'Buff Failed',font=(None,20))
        elif HT.label=='Enrage':
            l1 = canvas73.create_text(1000-x,y,fill="#0f0",text='Defence +50\nAttack +50',font=(None,20))
            w2.atkdrift(+50)
            w2.blockdrift(+50)
        elif HT.label=='Dissendium':
            if hit[-1] == -1: TankB.blockdrift(-10)
            l1 = canvas73.create_text(x,y,fill="#f10",text='Defence -10' if hit[-1] == -1 else 'Nerf Failed',font=(None,20))
        elif HT.label=='Reparo':
            l1 = canvas73.create_text(1000-x,y,fill="#0f0",text='+15' if hit[-1] == -1 else 'Heal Failed',font=(None,20))
            if hit[-1] == -1: TankA.takeDamage(-1,15)
        elif HT.label=='LumosMaxima':
            l1 = canvas73.create_text(x,y,fill="#ff0",text='Accuracy -10%' if hit[-1] == -1 else 'Nerf Failed',font=(None,20))
        elif HT.label=='Imperio':
            l1 = canvas73.create_text(x,y,fill="#f00",text='Imperius Curse!' if hit[-1] == -1 else 'Curse Failed',font=(None,20))
        elif HT.label=='PetrificusTotalus':
            l1 = canvas73.create_text(x,y,fill="#f00",text='Petrified!' if hit[-1] == -1 else 'Curse Failed',font=(None,20))
        elif HT.label=='Crucio':
            if hit[-1] == -1: TankB.poison += 3
            l1 = canvas73.create_text(x,y,fill="#f00",text='Infected!' if hit[-1] == -1 else 'Curse Failed',font=(None,20))
        canvas73.after(800,lambda: canvas73.delete(l1))
        
        if HT.label == 'Levicorpus' and hit[-1]>0:
            l2 = canvas73.create_text(1000-x,y,fill="#0f0",text='+10',font=(None,25))
        elif HT.label == 'SalvioHexia' and dmg[k]>0:
            l2 = canvas73.create_text(1000-x,y,fill="#0f0",text=f'+{dmg[k]}',font=(None,25))
        elif HT.label == 'Diffindo' and hit[-1]>0:
            l2 = canvas73.create_text(1000-x,y,fill="#0f0",text='Defence +5',font=(None,25))
            TankA.blockdrift(+5)
        elif HT.label == 'Incendio' and hit[-1]>0:
            TankA.atkdrift(+2)
            l2 = canvas73.create_text(1000-x,y,fill="#0f0",text='Attack +2',font=(None,25))
        elif HT.label == 'Revelio' and hit[-1]>0 and accurate(0.2):
            TankB.atkdrift(-5)
            TankB.blockdrift(-5)
            TankB.acc -= 0.05
            l2 = canvas73.create_text(x,y,fill="#ff0",text='Attack -5\nDefence -5\n Accuracy -5%',font=(None,25))
        else: l2 = canvas73.create_text(x,y,fill="#ff0",text='')
        canvas73.after(800,lambda: canvas73.delete(l2))
        if HT.type != 'A':
            k = n = 0
            dmg, hit, HT = [0], [0], 'nil'
            ChangeGameState()

    if GameState == 100: # If the one of the players dies
        messagebox.config(text = f'{TankA} wins!')
        TankB.lose()
        canvas73.create_text(500,150,text=f"\n{TankA} wins!",font=('showcard gothic',50),fill="#ff0")
        TankA.move(1500)
        
    elif GameState == -100:
        TankB.lose()
        if TankA == w1:
            global level
            TankA.move(1500)
            messagebox.config(text = 'YOU ARE VICTORIOUS!')
            canvas73.create_text(500,150,text="\nVICTORY!",font=('showcard gothic',50),fill="#ff0")
            level = w1.level
            y = w1.health//10 if w1.level < 25 else 3*w1.health//20
            y += 10 if w2.colour == 'brown' else 2
            x = f'{y}' if (w1.level==25 and data.userlist[w1.name].ladder<=5) else f'{y}\n{w1}.xp+={y//2}'
            x += f"\n{w1}.ladder+=1" if w2.colour == 'brown' else ''
            datafile = open('data.py', mode='a', encoding='utf-8') # updating data
            datafile.write(f'\n{w1}.coins+={x}')
            datafile.close()
            canvas73.after(3000,ChangeGameState)
        else:
            messagebox.config(text = 'YOU LOSE!')
            canvas73.create_text(500,150,text="\nYOU LOSE!",font=('showcard gothic',50),fill="#ff0")
    
    elif GameState == -80:
        global w1check
        w1check = True # w1check has to be made true again for next game
        importlib.reload(data)
        h = w1.health
        w = data.userlist[w1.name]
        levelup=False
        if level < w1.level:
            levelup = True
        load(game_window,game_frame,w.name,menu)
        if not (w2.colour == "brown" or levelup):
            w1.takeDamage(1,w1.maxHealth-h)

def ChangeGameState(x=None,*args):
    global GameState
    if type(x)==int:
        GameState = x
        return
    elif TankB.health == 0 and abs(GameState) == 2: GameState = 100*sgm(GameState) # Opponent just died? That's game over!
    elif abs(GameState) == 1: GameState = 10*sgm(GameState) # This calls the beam when an attack is clicked
    elif abs(GameState) == 10: GameState = 2*sgm(GameState) # This causes blast when beam hits the opponent tank
    elif abs(GameState) == 2: GameState = 1*sgm(GameState) # Switches back to ATTACK mode
    elif GameState == -100: GameState = -80 # on boss defeat

    SetGame() # Applying changes in GameState

'---------------------------LOAD FUNCTIONS---------------------------'

def LoadObjects():
    global canvas73,messagebox
    #canvas73.create_text(500,80,text='T A N K S',fill='#ff0',font=('showcard gothic',80))
    x = randint(200,800)
    y = randint(100,150)
    for i in range(100):
        canvas73.create_text(1000*random(),300*random(),fill="#fff",text="*") # stars
    create_circle(x,y,40,canvas73,'#bbb')
    create_circle(x+45,y-25,65,canvas73,'#000')
    w1.tank(canvas73)
    w2.tank(canvas73)
    canvas73.create_rectangle(0,355 , 1000,405 , fill="#a52a2a") # ground

def LoadTitle():
    T=canvas73.create_polygon(80,20,80,30,100,30,100,80,110,80,110,30,130,30,130,20,80,20,outline="#ffff00")

    A_left1=canvas73.create_line(170,20,140,80,fill="#ffff00")
    A_left2=canvas73.create_line(170,40,160,80,fill="#ffff00")
    A_right1=canvas73.create_line(170,40,180,80,fill="#ffff00")
    A_right2=canvas73.create_line(170,20,200,80,fill="#ffff00")
    A_bot1=canvas73.create_line(140,80,160,80,fill="#ffff00")
    A_bot2=canvas73.create_line(180,80,200,80,fill="#ffff00")

    N=canvas73.create_polygon(210,20,210,80,220,80,220,40,240,80,250,80,250,20,240,20,240,75,220,20,210,20,outline='#ffff00')

    K=canvas73.create_polygon(260,20,260,80,267,80,267,50,277,80,285,80,275,50,275,40,285,20,277,20,267,40,267,20,260,20,outline='#ffff00')

    S=canvas73.create_polygon(295,20,315,20,315,30,300,30,300,50,315,50,315,80,295,80,295,75,310,75,310,55,295,55,295,20,outline='#ffff00')
    
def LoadGame(root,frame,f):
    global canvas73,canvas2x,a1,a2,a3,a4,a5,messagebox,canvas2x,game_frame,menu
    menu = f
    frame.destroy()
    ChangeGameState(50) # this state will shift the tanks out of the screen from where they will move to acquire positions
    
    game_frame = Frame(root)
    game_frame.pack()

    frame=Frame(game_frame) # this frame contains player labels (name,level,health)
    frame.pack()

    canvas2x = Canvas(game_frame, bg="#000", width = 1000, height = 10) # health bars
    canvas2x.pack()

    canvas73 = Canvas(game_frame,width=1000,height=405,bg="#000") # TANKS appear here
    canvas73.pack()

    w1.Labels(canvas2x,frame,1) # creating player labels
    w2.Labels(canvas2x,frame,2)

    LoadObjects() # creating TANKS and background (stars,moon)
    
    frame3 = Frame(game_frame, bg = '#000') # this is where the messages are added
    frame3.pack()
    messagebox = Label(frame3, bg = '#000', fg = '#fff', width = 143, height = 4,font=("courier",10))
    messagebox.pack()

    frame4 = Frame(game_frame, bg = '#000',width=1000,height=5) # and attacks of course
    frame4.pack_propagate(0)
    frame4.pack()
    a1f = Frame(frame4,width=200,height=50,bg="#000") # creating seperate frame from each attack button to prevent them overflow off the screen
    a2f = Frame(frame4,width=200,height=50,bg="#000")
    a3f = Frame(frame4,width=200,height=50,bg="#000")
    a4f = Frame(frame4,width=200,height=50,bg="#000")
    a5f = Frame(frame4,width=200,height=50,bg="#000")
    a1f.pack_propagate(0)
    a2f.pack_propagate(0)
    a3f.pack_propagate(0)
    a4f.pack_propagate(0)
    a5f.pack_propagate(0)
    a1f.grid(row=1,column=1)
    a2f.grid(row=1,column=2)
    a3f.grid(row=1,column=3)
    a4f.grid(row=1,column=4)
    a5f.grid(row=1,column=5)
    a1 = Label(a1f, width = 25, height = 3, fg = '#fff', bg = 'grey', border = 0,font=("courier",12))
    a2 = Label(a2f, width = 25, height = 3, fg = '#fff', bg = 'grey', border = 0,font=("courier",12))
    a3 = Label(a3f, width = 25, height = 3, fg = '#fff', bg = 'grey', border = 0,font=("courier",12))
    a4 = Label(a4f, width = 25, height = 3, fg = '#fff', bg = 'grey', border = 0,font=("courier",12))
    a5 = Label(a5f, width = 25, height = 3, fg = '#fff', bg = 'grey', border = 0,font=("courier",12))
    a1.pack()
    a2.pack()
    a3.pack()
    a4.pack()
    a5.pack()
    
    root.bind("<Escape>",lambda x: menu(game_frame))

    return game_frame,canvas73
