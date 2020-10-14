"""---------------CREATED BY DIVYAM JOSHI AND K ADITYA----------------"""
"""------------------------CURRENT VERSION : 7------------------------"""
"""-------------------------UPDATED 15/05/2020------------------------"""

# you can download and make contributions to the game from Divyam's GitHub repository https://github.com/iamgroot9/iamgroot
from survival import *
from campaign import *

"======================================== MENU ========================================"

def menu(iframe):
    game_window.bind("<Return>",DoNothing)
    game_window.bind("<Escape>",DoNothing)
    ChangeGameState(0)
    iframe.destroy()
    introFrame = Frame(game_window, bg="#000",width=1000,height=600)
    introFrame.pack_propagate(0)
    introFrame.pack()
    Label(introFrame, bg = "#000", text = "T A N K S", fg = "#ff0", border=5, font=('showcard gothic',60)).pack()
    x1 = Label(introFrame, bg = "#000", text = "Campaign", fg = "#fff", cursor = 'hand2', border=3, font=('courier',30,'bold'))
    x2 = Label(introFrame, bg = "#000", text = "Survival", fg = "#fff", cursor = 'hand2', border=3, font=('courier',30,'bold'))
    x3 = Label(introFrame, bg = "#000", text = "Two Player", fg = "#fff", cursor = 'hand2', border=3, font=('courier',30,'bold'))
    x4 = Label(introFrame, bg = "#000", text = "Profile", fg = "#fff", cursor = 'hand2', border=3, font=('courier',30,'bold'))
    x5 = Label(introFrame, bg = "#000", text = "Log Out", fg = "#fff", cursor = 'hand2', border=3, font=('courier',30,'bold'))
    x6 = Label(introFrame, bg = "#000", text = "Exit", fg = "#fff", cursor = 'hand2', border=3, font=('courier',30,'bold'))
    x1.bind("<Button-1>",lambda x: LoadMap(game_window,introFrame,userx,menu))
    x2.bind("<Button-1>",lambda x: LoadMatchS(game_window,introFrame,userx,menu))
    x3.bind("<Button-1>",lambda x: LoadMatch2p(game_window,introFrame,menu))
    x4.bind("<Button-1>",lambda x: ProfileScreen(introFrame))
    x5.bind("<Button-1>",lambda x: LoginScreen(introFrame))
    x6.bind("<Button-1>",lambda x: quit())
    x1.bind("<Enter>",lambda x: on_enter(x1))
    x2.bind("<Enter>",lambda x: on_enter(x2))
    x3.bind("<Enter>",lambda x: on_enter(x3))
    x4.bind("<Enter>",lambda x: on_enter(x4))
    x5.bind("<Enter>",lambda x: on_enter(x5))
    x6.bind("<Enter>",lambda x: on_enter(x6))
    x1.bind("<Leave>",lambda x: on_leave(x1))
    x2.bind("<Leave>",lambda x: on_leave(x2))
    x3.bind("<Leave>",lambda x: on_leave(x3))
    x4.bind("<Leave>",lambda x: on_leave(x4))
    x5.bind("<Leave>",lambda x: on_leave(x5))
    x6.bind("<Leave>",lambda x: on_leave(x6))
    x1.pack()
    x2.pack()
    x3.pack()
    x4.pack()
    x5.pack()
    x6.pack()
    fx2 = Canvas(introFrame,width=560, height = 35, bg = '#000',highlightbackground="#000")
    fx2.pack(side=BOTTOM)
    fx2.create_text(307.5,10,fill="#1f0",text=f"Logged In as {userx}")
    fx2.create_text(307.5,25,fill="#1f0",text=f"TANKS v{version}  |  (c) 2019-2020  |  Divyam Joshi  |  K Aditya")

"======================================== LOGIN ========================================"

def LoginScreen(*x):
    if x: x[0].destroy()
    global LoginFrame, name, login_message, pass1
    LoginFrame = Frame(game_window, bg = '#000',height=600,width=1000)
    LoginFrame.pack_propagate(0)
    LoginFrame.pack()
    Label(LoginFrame, bg = "#000", text = "T A N K S", fg = "yellow", border=5, font=('showcard gothic',60)).pack()
    f1 = Frame(LoginFrame,bg="#000")
    f1.pack()
    Label(f1,text = "Username: ",bg="#000",fg="#fff").grid(row=1,column=1)
    name = Entry(f1)
    name.grid(row=1,column=2)
    Label(f1, bg = '#000', fg = '#fff', text = 'Password: ').grid(row=2,column=1)
    pass1 = Entry(f1, show = '*') # and this is where password is entered
    pass1.grid(row=2,column=2)
    Frame(LoginFrame, height = 10, bg = '#000').pack()
    f3 = Frame(LoginFrame, bg = '#000')
    login_message = Label(f3, bg='#000', fg='#ff0000')
    login_message.pack()
    f3.pack()
    Button(f3, text = 'Login', bg = '#000', fg = '#1f0', command = Login, cursor = 'hand2').pack()
    game_window.bind('<Return>',lambda x: Login()) # press enter to login
    fx2 = Canvas(LoginFrame,width=560, height = 35, bg = '#000',highlightbackground="#000")
    fx2.pack(side=BOTTOM)
    fx2.create_text(307.5,25,fill="#1f0",text=f"TANKS v{version}  |  (c) 2019-2020  |  Divyam Joshi  |  K Aditya")

def Login(*args):
    global login_message,u1,u2,w1,w2 # in case player enters incorrect password, this would be configred to display the message
    p = pass1.get() # pass1 is the entry box which recieve entered password
    passcheck = True
    uname = ''
    user = name.get() # name is the entry box which recieve entered username
    password = encode(p)
    for i in range(len(user)): # correcting usernames to prevent entry of bad data
        if ( not user[i].isalnum() ): uname+='_' # bad data will be converted to _
        else: uname+=user[i]
    if len(user)==0:
        login_message.config(text='Invalid username(s)!')
        return

    if uname in data.userlist: # check passwords for registered users
        if data.userlist.get(uname).password != password: passcheck = False
    elif uname not in data.bosslist+list(data.abilitylist): # register new users
        datafile = open('data.py', mode='a', encoding = 'utf-8')
        datafile.write(f'\n{uname}=Player("{uname}","{password}")\nuserlist["{uname}"]={uname}')
        datafile.close()
    else:
        login_message.config(text='Invalid username(s)!')
        return

    importlib.reload(data) # loads modified data file with new users registered

    if passcheck:
        global userx
        userx = uname
        menu(LoginFrame)
    else: login_message.config(text='Password(s) entered are incorrect!')

"======================================== PROFILE ========================================"

def ProfileScreen(iframe, *x):
    if x:
        datafile = open('data.py', mode='a', encoding='utf-8') # updating data
        datafile.write(f'\n{userx}.colour = "{x[0]}"')
        datafile.close()
        importlib.reload(data)
    
    def confirm(frame,x):
        d = {'h':'Health' , 'a':'Attack' , 'b':'Defence'}
        messagebox.config(text=f'Are you sure you want to upgrade your {d[x]}?\nThis change can not be reversed.')
        confirmbox = Label(extraframe2,bg="#000",fg='#fff',text='Confirm',cursor='hand2',font=('courier',15))
        space = Label(extraframe2,bg="#111",fg='#fff',text='    ',font=('courier',15))
        denybox = Label(extraframe2,bg="#000",fg='#fff',text='Deny',cursor='hand2',font=('courier',15))
        confirmbox.grid(row=1,column=1)
        space.grid(row=1,column=2)
        denybox.grid(row=1,column=3)
        denybox.bind("<Button-1>",lambda w: ProfileScreen(frame))
        confirmbox.bind("<Button-1>",lambda w: update_stats(frame,x))

    def update_stats(frame,x):
        datafile = open('data.py', mode='a', encoding='utf-8') # updating data
        datafile.write(f'\n{userx}.{x}buff += 1')
        datafile.close()
        importlib.reload(data)
        ProfileScreen(frame)

    ChangeGameState(0)
    iframe.destroy()
    frame = Frame(game_window,bg="#000",height = 600, width = 1000)
    frame.pack_propagate(0)
    frame.pack()
    player = data.userlist[userx]
    frame2 = Frame(frame,bg="#000")
    frame2.pack(side=TOP)
    canvas = Canvas(frame2,height=250,width=300,bg="#000",highlightbackground="#0a0a0a",cursor="hand2",border=1)
    canvas.grid(row=2,column=1)
    canvas.create_text(90,225,fill="#1f0",text="CHANGE")
    Tank(player).tank(canvas)
    canvas.bind("<Button-1>",lambda x: selectColour(frame,Tank(player)))
    Label(frame2,bg="#000",fg="#ff0",text=f"PROFILE OF: {userx}",font=("courier",35)).grid(row=1,column=1,columnspan=3)
    
    frame3 = Frame(frame2,bg="#000",border=20)
    frame3.grid(row=2,column=2)
    Label(frame3,bg="#000",fg="#fff",text=f"Health: {player.maxHealth}\nAttack: {player.maxAtk}\nDefence: {player.maxBlock}\nCoins: {player.coins}",font=('courier',18)).grid(row=2,column=1)
    canvas1 = Canvas(frame3,bg='grey',width=200,height=30)
    canvas1.grid(row=1,column=1)
    if (player.level < 25) or (player.ladder > 5):
        l = player.level
        cxp = player.xp - l**2
        rxp = 2 * l + 1
        bar = (cxp/rxp)*200
        canvas1.create_rectangle(0,0,bar,15,fill="#0f0")
        canvas1.create_text(30,22,text=f"Level: {l}")
        canvas1.create_text(170,22,text=f"Level: {l+1}")
    else:
        canvas1.create_rectangle(0,0,200,15,fill="#0f0")
        canvas1.create_text(100,7,text="MAX LEVEL")
        canvas1.create_text(100,22,text="Level: 25")
        
    frameb = Frame(frame2,bg="#000",width=200,height=300,border = 50)
    frameb.pack_propagate(0)
    frameb.grid(row=2,column=3)
    Label(frameb,bg="#000",fg="#1f0",text=f"Upgrade\nAvailable: {player.buff}",font=("courier",18)).grid(row=1,column=1)
    if player.buff > 0:
        hbuff = Label(frameb,bg="#000",fg="#fff",text="Health +5",relief='groove',font=("courier",18),cursor="hand2")
        hbuff.grid(row=2,column=1)
        abuff = Label(frameb,bg="#000",fg="#fff",text="Attack +5",relief='groove',font=("courier",18),cursor="hand2")
        abuff.grid(row=3,column=1)
        bbuff = Label(frameb,bg="#000",fg="#fff",text="Defence +5",relief='groove',font=("courier",18),cursor="hand2")
        bbuff.grid(row=4,column=1)
        hbuff.bind("<Enter>",lambda x: on_enter(hbuff))
        hbuff.bind("<Leave>",lambda x: on_leave(hbuff))
        abuff.bind("<Enter>",lambda x: on_enter(abuff))
        abuff.bind("<Leave>",lambda x: on_leave(abuff))
        bbuff.bind("<Enter>",lambda x: on_enter(bbuff))
        bbuff.bind("<Leave>",lambda x: on_leave(bbuff))
        hbuff.bind("<Button-1>",lambda x: confirm(frame,'h'))
        abuff.bind("<Button-1>",lambda x: confirm(frame,'a'))
        bbuff.bind("<Button-1>",lambda x: confirm(frame,'b'))
    else: Label(frameb,bg="#000",fg="#f00",text="No upgrades available",font=("courier",15)).grid(row=2,column=1)
    
    aframe = Frame(frame2,bg="#000",width=1000,height=100,border = 20)
    aframe.grid(row=3,column=1,columnspan=5)
    Label(aframe,bg="#000",fg="yellow",text='Skillset:',font=("courier",18)).pack(side=TOP)
    Label(aframe,bg="#000",fg="#fff",text=f"{player.a1}  |  {player.a2}  |  {player.a3}  |  {player.a4}  |  {player.a5}",font=("courier",18)).pack()
    aedit = Label(aframe,bg="#000",fg="#1f0",text='Edit',font=("courier",18),cursor="hand2")
    aedit.pack(side=BOTTOM)
    aedit.bind("<Button-1>",lambda x: selectAtks(frame,player))
    
    extraframe = Frame(frame2,bg="#111",width=800,height=100)
    extraframe.pack_propagate(0)
    extraframe.grid(row=4,column=1,columnspan=3)
    extraframe1 = Frame(extraframe,bg="#111",width=800,height=70)
    extraframe1.pack_propagate(0)
    extraframe1.pack()
    messagebox = Label(extraframe1,bg="#111",fg="#fff",text="Press Escape or Enter to get back to menu",font=("courier",15))
    messagebox.pack()
    extraframe2 = Frame(extraframe,bg="#111",width=800,height=30)
    extraframe2.pack_propagate(0)
    extraframe2.pack()

    game_window.bind("<Escape>",lambda x: menu(frame))
    game_window.bind("<Return>",lambda x: menu(frame))
    fx2 = Canvas(frame,width=560, height = 35, bg = '#000',highlightbackground="#000")
    fx2.pack(side=BOTTOM)
    fx2.create_text(307.5,25,fill="#1f0",text=f"TANKS v{version}  |  (c) 2019-2020  |  Divyam Joshi  |  K Aditya")

"======================================== COLOUR SELECTION ========================================"

def selectColour(framei,w1):
    global colour_panel,colour_state,canvas_panel

    framei.destroy()
    frame=Frame(game_window,bg='#000')
    frame.pack()
    frame.pack_propagate(0)
    
    Label(frame,bg="#000",fg="#fff",text='Select you tank', font=(None,20)).grid(row=0,column=1)
    Label(frame,bg="#000",fg="#fff",text=f'{w1}').grid(row=1,column=1)
    
    w1Canvas = Canvas(frame,bg='#000')
    w1Canvas.grid(row = 2, column = 1)
    
    blue1=Canvas(w1Canvas, bg='#000', width=500, height=250, highlightbackground = "#000")
    blue1.grid(row=1,column=1)
    green1=Canvas(w1Canvas, bg='#000', width=500, height=250, highlightbackground = "#000")
    green1.grid(row=1,column=2)
    red1=Canvas(w1Canvas, bg='#000', width=500, height=250, highlightbackground = "#000")
    red1.grid(row=2,column=1)
    orange1=Canvas(w1Canvas, bg='#000', width=500, height=250, highlightbackground = "#000")
    orange1.grid(row=2,column=2)
    
    colour_state=[0,0]
    canvas_panel=[[blue1,green1],[red1,orange1]]
    colour_panel=[['#00f','#080'],['#f00','#f70']]
    
    def setColour1p(canvas,colour,arg1,arg2):
        global colour_state
        colour_state=[arg1,arg2]
        w1.colour = colour
        for i in [blue1,green1,red1,orange1]:
            if i == canvas: continue
            else: i.config(highlightbackground = "#000")
        canvas.config(highlightbackground = '#ff0')
        if found: ws.PlaySound('btn_click.wav', ws.SND_FILENAME | ws.SND_ASYNC)
        else: sp.Popen(['afplay','btn_click.wav'])
        
    def setColour1p_arrow(a):
        global colour_panel,colour_state,canvas_panel
        if a=='Up':
            colour_state=[abs(colour_state[0]-1)%2,abs(colour_state[1])%2]
        elif a=='Down':
            colour_state=[abs(colour_state[0]+1)%2,abs(colour_state[1]%2)]
        elif a=='Left':
            colour_state=[abs(colour_state[0])%2,abs(colour_state[1]-1)%2]
        elif a=='Right':
            colour_state=[abs(colour_state[0])%2,abs(colour_state[1]+1)%2]
        setColour1p(canvas_panel[colour_state[0]][colour_state[1]],colour_panel[colour_state[0]][colour_state[1]],colour_state[0],colour_state[1])
        
    w1.tank(blue1,"#00f")
    w1.tank(red1,"#f00")
    w1.tank(green1,"#080")
    w1.tank(orange1,"#f70")
    
    blue1.bind("<Button-1>",lambda x: setColour1p(blue1,'#00f',0,0))
    red1.bind("<Button-1>",lambda x: setColour1p(red1,'#f00',1,0))
    green1.bind("<Button-1>",lambda x: setColour1p(green1,'#080',0,1))
    orange1.bind("<Button-1>",lambda x: setColour1p(orange1,'#f70',1,1))
    game_window.bind("<Up>",lambda e:setColour1p_arrow('Up'))
    game_window.bind("<Down>",lambda e:setColour1p_arrow('Down'))
    game_window.bind("<Left>",lambda e:setColour1p_arrow('Left'))
    game_window.bind("<Right>",lambda e:setColour1p_arrow('Right'))
    setColour1p(blue1,'#00f',0,0)
    
    Button(frame,text="OK",command = lambda: ProfileScreen(frame,w1.colour)).grid(row=3,column=1)
    game_window.bind('<Return>',lambda x: ProfileScreen(frame,w1.colour))
    game_window.bind("<Escape>",lambda x: ProfileScreen(frame))

"======================================== ABILITY SELECTION ========================================"

def selectAtks(framex,player):
    global messagebox
    framex.destroy()
    
    class AtkCell:
        def __init__(self,master,a,r,c):
            self.a = a
            self.frame = Frame(master,width=200,height=50,bg="#000")
            self.frame.pack_propagate(0)
            self.frame.grid(row=r,column=c)
            self.col = "#fff" if player.level >= a.rlevel else "#888"
            self.label = Label(self.frame,bg="#000",fg=self.col,text=self.a.label,font=("courier",15),width=25)
            self.label.pack()
            self.label.bind("<Enter>",lambda x: on_enter(self.label,self.a,messagebox))
            self.label.bind("<Leave>",lambda x: on_leave(self.label,self.col))
            if self.a.rlevel <= player.level: self.label.bind("<Button-1>",lambda x: select(self))
            else: self.label.bind("<Button-1>",lambda x: locked(self))
    def select(a):
        messagebox.config(text="Select the skill you wish to replace from above")
        for i in newlist2:
            i.label.config(fg=i.col)
        a.label.config(fg='#ff0')
        a.label.bind("<Leave>",DoNothing)
        a.label.bind("<Enter>",DoNothing)
        newlist[0].label.bind("<Button-1>",lambda x: replace(a.a , 1))
        newlist[1].label.bind("<Button-1>",lambda x: replace(a.a , 2))
        newlist[2].label.bind("<Button-1>",lambda x: replace(a.a , 3))
        newlist[3].label.bind("<Button-1>",lambda x: replace(a.a , 4))
        newlist[4].label.bind("<Button-1>",lambda x: replace(a.a , 5))
    def replace(x,y):
        datafile = open('data.py', mode='a', encoding='utf-8') # updating data
        datafile.write(f'\n{userx}.a{y} = {x.label.lower()}')
        datafile.close()
        importlib.reload(data)
        player = data.userlist[userx]
        selectAtks(frame,player)
    def locked(a):
        messagebox.config(text=f'Unlocks at level {a.a.rlevel}',fg="#f00")
        a.label.config(fg="#f00")

    frame = Frame(game_window,bg="#000",height = 600, width = 1000)
    frame.pack_propagate(0)
    frame.pack()
    
    frame1 = Frame(frame,bg="#000",height = 140, width = 1000)
    frame1.pack_propagate(0)
    frame1.pack()
    Label(frame1,bg="#000",fg="yellow",text="SKILLSET",font=("courier",35)).grid(row=0,column=0,columnspan=5)
    Label(frame1,bg="#000",fg="#ff0",text="Equipped:",font=("courier",25)).grid(row=1,column=0,columnspan=5)
    newlist = []
    for a in range(len(player.skillset)):
        q = AtkCell(frame1,player.skillset[a],2,a)
        q.label.bind("<Button-1>",DoNothing)
        newlist.append(q)

    frame2 = Frame(frame,bg="#000",height = 100, width = 1000)
    frame2.pack_propagate(0)
    frame2.pack()
    messagebox = Label(frame2,bg="#111",height=100,width=1000,fg="#fff",text="Select the skill you wish to add from below",font=("courier",15))
    messagebox.pack()
    
    frame3 = Frame(frame,bg="#000",height = 360, width = 1000)
    frame3.pack_propagate(0)
    frame3.pack()
    Label(frame3,bg="#000",fg="#ff0",text="Inventory:",font=("courier",25)).grid(row=0,column=0,columnspan=5)
    l = data.abilitylist
    a = 0
    newlist2 = []
    for i in l:
        if l[i] not in player.skillset:
            if i == 'enrage': continue
            q = AtkCell(frame3,l[i],1 + (a)//5, a%5)
            newlist2.append(q)
            a+=1
    game_window.bind("<Escape>",lambda x: ProfileScreen(frame))
    game_window.bind("<Return>",lambda x: ProfileScreen(frame))
    
    
'---------------------------TWO PLAYER---------------------------'

def LoadMatch2p(game_window,frame,menu):
    global canvas73,canvas2x,a1,a2,a3,a4,messagebox,canvas2x,w1,w2
    ChangeGameState(40)
    w1 = Tank('Player 1')
    w2 = Tank('Player 2')
    w1.colour = choice(['Pink','Red','Blue','Green','Orange','Indigo','Magenta','Aqua'])
    while True:
        w2.colour = choice(['Pink','Red','Blue','Green','Orange','Indigo','Magenta','Aqua'])
        if w1.colour != w2.colour: break
        
    mainframe,canvas73 = LoadGame(game_window,frame,menu)
    
    w1.move(400)
    w2.move(400)
    canvas73.after(2000,lambda: LoadMatch2())
    
def LoadMatch2():
    ChangeGameState(1)
    SetGame()

game_window = Tk()
game_window.title("TANKS v" + version)
game_window.geometry('1000x600')
game_window.resizable(0,0)
LoginScreen()
game_window.mainloop()