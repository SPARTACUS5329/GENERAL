from Global import *

def LoadMatchS(root,frame,user,menu):
    global canvas73,game_window,canvas2x,a1,a2,a3,a4,messagebox,game_window,canvas2x
    game_window = root
    ChangeGameState(40)
    u = data.userlist[user]
    w1 = Tank(u)
    bot = data.Player(choice(['Dexter','Mojin','Nexus','Jack','Banner','Butcher','Shogun','Dues','McLeen','Hermit','Barboss','Nox']),'xyz')
    bot.xp = u.xp
    while bot.buff > 0:
        z = randint(1,4)
        if z==1: bot.hbuff += 1
        elif z==2: bot.bbuff += 1
        elif z==3: bot.abuff += 1
    while True:
        bot.colour = choice(['Pink','#f00','#00f','#080','#570','Indigo','Magenta','Aqua'])
        if w1.colour != bot.colour: break
    botatklist = []
    while len(botatklist) < 3: # for damaging attacks
        z = choice(list(data.abilitylist.values()))
        if z.rlevel > bot.level or z in botatklist or z.dmg == 0:
            continue
        else:
            botatklist.append(z)
    while len(botatklist) < 5: # for any random attack
        z = choice(list(data.abilitylist.values()))
        if z.rlevel > bot.level or z in botatklist:
            continue
        else:
            botatklist.append(z)
    bot.a1, bot.a2, bot.a3, bot.a4, bot.a5 = botatklist
    
    w2 = Tank(bot)
    
    mainframe,canvas73 = LoadGame(game_window,frame,menu)

    w1.move(400)
    w2.move(400)
    t = canvas73.create_text(500,250,text=f"{w1}   vs   {w2}",fill="yellow",font=("showcard gothic",60))
    canvas73.after(2000,lambda: canvas73.delete(t))
    canvas73.after(2000,LoadMatch2)
    
def LoadMatch2():
    global a1,a2,a3,a4,messagebox,game_window,canvas2x
    
    ChangeGameState(-1)
    SetGame(game_window,LoadMatchS)
