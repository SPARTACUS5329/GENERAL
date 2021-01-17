import math

"------------------------------ABILITIES------------------------------"

class ability:
    def __init__(self,label,dmg,acc,boom=1,rlevel=1,t='A'):
        self.label = label
        self.dmg = dmg
        self.acc = acc
        self.boom = boom
        self.type = t
        self.colour = '#f00' if dmg > 20 else '#f30' if dmg >= 15 else '#fc0'
        self.rlevel = rlevel
        c = 'A powerful recursive attack' if boom > 1 else 'A strong attack' if dmg > 20 else 'A moderately powerful attack' if dmg > 15 else 'An attack' if dmg > 0 else ''
        c += ' with high accuracy' if acc > 0.8 else ' with moderate accuracy' if acc > 0.7 else ''
        if boom > 1: dmg=f'{dmg}x{boom}'
        self.comment = f"{c}\nAttack Power: {dmg}\nAccuracy: {(int(acc*100))}%"
        abilitylist[self.label.lower()] = self
    def __str__(self):
        return self.label

abilitylist = {}

stupefy = ability("Stupefy",dmg=10,acc=1)

confringo = ability("Confringo",dmg=20,acc=0.7)

reducto = ability("Reducto",dmg=30,acc=0.45)

bombarda = ability("Bombarda",dmg=15,acc=0.8)

incendio = ability("Incendio",dmg=10,acc=0.9)
incendio.comment += "\nImproves ability power by 2"

expulso = ability("Expulso",dmg=23,acc=0.65,rlevel=6)

reparo = ability("Reparo",dmg=0,acc=0.9,t='H',rlevel=8)
reparo.comment = "Heal: +15 health\nAccuracy: 90%"

revelio = ability("Revelio",dmg=12,acc=0.85,rlevel=9)
revelio.comment += "\n20% Chance of wreak havoc"

levicorpus = ability("Levicorpus",dmg=10,acc=0.75,rlevel=12)
levicorpus.comment = "An attack with healing powers\nAttack Power: 10\nHeal: 15\n Accuracy: 70%"

lumosmaxima = ability("LumosMaxima",dmg=0,acc=0.7,rlevel=13,t='N')
lumosmaxima.comment = "Reduces the opponent's accuracy by 10%\nAccuracy: 70%"

protego = ability("Protego",dmg=0,acc=0.95,rlevel=15,t='B')
protego.comment = "Improves player's defence by 10\nAccuracy: 95%"

sectumsempra = ability("Sectumsempra",dmg=18,acc=0.6,boom=2,rlevel=15)

salviohexia = ability("SalvioHexia",dmg=4,acc=0.7,boom=4,rlevel=17)
salviohexia.comment = "An ability that transfers the opponent's health to you\nAttack Power: 4x4\nAccuracy: 70%"
salviohexia.colour = '#1f0'

diffindo = ability("Diffindo",dmg=25,acc=0.5,rlevel=18)
diffindo.comment += "\nImproves defence by 5"

imperio = ability("Imperio",dmg=0,acc=0.5,t='C',rlevel=19)
imperio.comment = "A curse that causes the opponent to lose control for 2 turns\nAccuracy: 50%"

petrificustotalus = ability("PetrificusTotalus",0,0.5,rlevel=20,t='C')
petrificustotalus.comment = "A curse that prevents the opponent from playing next 2 turns\nAccuracy: 50%"

dissendium = ability("Dissendium",dmg=0,acc=0.9,t='N',rlevel=21)
dissendium.comment = "Reduces the opponent's defence by 10\nAccuracy: 90%"

crucio = ability("Crucio",dmg=0,acc=0.8,t='C',rlevel=24)
crucio.comment = "The opponent takes damage over time\nDamage: 10x3\nAccuracy: 80%"

bombardamaxima = ability("BombardaMaxima",dmg=3,acc=0.85,boom=10,rlevel=25)

enrage = ability("Enrage",dmg=0,acc=1,rlevel=30,t='B') # FINAL BOSS ONLY, +50 ability and defence

"-----------------------------BOSS DATA-----------------------------"

class Boss:
    def __init__(self,name,health,atk,block,level,a1,a2,a3,a4,a5):
        self.maxHealth = health
        self.name = name
        self.maxAtk = atk
        self.maxBlock = block
        self.level = level
        self.colour = "brown"
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a5 = a4

boss1=Boss("Marrow",130,40,40,10,confringo,bombarda,reducto,incendio,levicorpus)
boss2=Boss("Gabriel",140,80,35,15,levicorpus,stupefy,confringo,bombarda,incendio)
boss3=Boss("Le Raux",150,55,50,20,reducto,expulso,confringo,protego,bombarda)
boss4=Boss("Wolvington",170,60,60,25,bombardamaxima,stupefy,levicorpus,protego,confringo)
boss5=Boss("Overlord",200,70,70,30,sectumsempra,bombardamaxima,expulso,enrage,bombarda)
bosslist = ['boss1','boss2','boss3','boss4','boss5']

"-----------------------------USER DATA-----------------------------"

class Player:
    
    def __init__(self, username, password,xp=1):
        self.name = username
        self.password = password
        self.ladder = 1
        self.xp = xp
        
        self.a1 = stupefy
        self.a2 = confringo
        self.a3 = bombarda
        self.a4 = reducto
        self.a5 = incendio
        
        self.colour = "#00f"
        
        self.hbuff = 0
        self.abuff = 0
        self.bbuff = 0
        self.xhbuff = 0
        self.xabuff = 0
        self.xbbuff = 0
        
        self.coins = 0
        
    @property
    def level(self):
        return int(self.xp ** 0.5)
    @property
    def maxHealth(self):
        return 99 + self.level + (self.hbuff+self.xhbuff)*5
    @property
    def maxBlock(self):
        return 19 + self.level + (self.bbuff+self.xbbuff)*5
    @property
    def maxAtk(self):
        return 19 + self.level + (self.abuff+self.xabuff)*5
    @property
    def boss(self):
        if self.ladder == 1: return boss1
        elif self.ladder == 2: return boss2
        elif self.ladder == 3: return boss3
        elif self.ladder == 4: return boss4
        else: return boss5
    @property
    def buff(self):
        return (self.level//3) + (self.level//5) - (self.hbuff + self.abuff + self.bbuff + (self.level//15))
    @property
    def skillset(self):
        return [self.a1 , self.a2 , self.a3 , self.a4 , self.a5]

userlist = {}

# there is automated code below this...

Divyam=Player("Divyam","0xaee4b272ce")
userlist["Divyam"]=Divyam
Divyam.xp+=624
SPARTACUS=Player("SPARTACUS","0x43c026e3f0a7aaa57")
userlist["SPARTACUS"]=SPARTACUS
SPARTACUS.xp+=624
a=Player("a","0x0")
userlist["a"]=a
a.xp += 200
Divyam.a1 = salviohexia
Divyam.a2 = bombardamaxima
Divyam.a3 = crucio
Divyam.a4 = sectumsempra
Divyam.a5 = reparo
Divyam.hbuff += 1
Divyam.bbuff += 1
Divyam.bbuff += 1
Divyam.bbuff += 1
Divyam.bbuff += 1
Divyam.abuff += 1
Divyam.abuff += 1
Divyam.abuff += 1
Divyam.abuff += 1
Divyam.abuff += 1
Divyam.abuff += 1
Divyam.abuff += 1
Divyam.coins+=10
Divyam.coins+=7
Divyam.coins+=7
Divyam.coins+=5
a.a1 = reparo
a.a3 = revelio
a.a2 = expulso
a.coins+=2
a.xp+=2
SPARTACUS.a5 = bombardamaxima
SPARTACUS.a3 = dissendium
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.bbuff += 1
SPARTACUS.coins+=10
TestUser=Player("TestUser","0x44bf764093d0e49a35aa57")
userlist["TestUser"]=TestUser
SPARTACUS.colour = "#00f"
SPARTACUS.coins+=12