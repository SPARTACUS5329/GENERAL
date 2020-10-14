from Global import *

class Map():
    def __init__(self,map_canvas,root):
        global player
        player=data.userlist.get(userx)
        self.map_canvas=map_canvas
        self.root=root
        self.root.bind('<Right>',lambda x:self.move(1,0))
        self.root.bind('<Left>',lambda x:self.move(-1,0))
        self.root.bind('<Up>',lambda x:self.move(0,-1))
        self.root.bind('<Down>',lambda x:self.move(0,1))
        self.y=0
        self.x=0
        if player.level < 10: self.tank=map_canvas.create_polygon(15,5 , 0,50 , 50,50 , 50,45 , 30,35 , 30,30 , 45,30 , 45,25 , 30,25 , 30,15 , 25,15 , 25,35 , 20,35 , 20,5 , fill=player.colour)
        elif player.level < 15: self.tank=map_canvas.create_polygon(15,5 , 0,50 , 50,50 , 50,45 , 30,35 , 30,30 ,    32,30 , 32,33 , 34,33 , 34,30 , 36,30 , 36,33 , 38,33 , 38,30 , 40,30 , 40,33 , 42,33 , 42,30    , 45,30 , 45,25 ,    42,25 , 42,22 , 40,22 , 40,25 , 38,25 , 38,22 , 36,22 , 36,25 , 34,25 , 34,22 , 32,22 , 32,25    , 30,25 , 30,15 , 25,15 , 25,35 , 20,35 , 20,5 , fill=player.colour)
        else: self.tank=map_canvas.create_polygon(15,5 , 0,50 , 50,50 , 50,45 , 30,35 , 30,30 ,    32,30 , 32,33 , 34,33 , 34,30 , 36,30 , 36,33 , 38,33 , 38,30 , 40,30 , 40,33 , 42,33 , 42,30    , 45,30 , 45,25 ,    42,25 , 42,22 , 40,22 , 40,25 , 38,25 , 38,22 , 36,22 , 36,25 , 34,25 , 34,22 , 32,22 , 32,25    , 30,25 , 30,20 , 45,20 , 45,15 , 30,15 , 25,15 , 25,35 , 20,35 , 20,5 , fill=player.colour)
        self.x_coord=0
        self.y_coord=0
        
    def move(self,x,y):
        if (x==-1 and self.x_coord==0) or (y==-1 and self.y_coord==0) or (x==1 and self.x_coord==950) or (y==1 and self.y_coord==550): return
        self.root.bind('<Right>',lambda x:DoNothing())
        self.root.bind('<Left>',lambda x:DoNothing())
        self.root.bind('<Up>',lambda x:DoNothing())
        self.root.bind('<Down>',lambda x:DoNothing())
        self.map_canvas.move(self.tank,x,y)
        self.x+=x
        self.y+=y
        self.x_coord+=x
        self.y_coord+=y
        if abs(self.x)<50 and abs(self.y)<50:
            self.map_canvas.after(1,lambda :self.move(x,y))
        else:
            self.x=self.y=0
            self.root.bind('<Right>',lambda x:self.move(1,0))
            self.root.bind('<Left>',lambda x:self.move(-1,0))
            self.root.bind('<Up>',lambda x:self.move(0,-1))
            self.root.bind('<Down>',lambda x:self.move(0,1))
        self.boss_check()
    def boss_check(self):
        boss_enter=False
        if self.x_coord==50 and self.y_coord==50 and player.ladder==1:
            boss_enter=True
        elif self.x_coord>=200 and self.x_coord<=250 and self.y_coord>=200 and self.y_coord<=250 and player.ladder==2:
            boss_enter=True
        elif self.x_coord>=500 and self.x_coord<=550 and self.y_coord==400 and player.ladder==3:
            boss_enter=True
        elif self.x_coord>=0 and self.x_coord<=350 and self.y_coord>=300 and self.y_coord<=550 and player.ladder==4:
            boss_enter=True
        if boss_enter:       
            introFrame = Frame(game_window, bg="#000",width=1000,height=600)
            introFrame.pack_propagate(0)
            introFrame.pack()
            LoadMatchC(game_window,introFrame,userx,menu)
            self.map_canvas.destroy()

def LoadMap(root,xframe,user,xmenu):
    global canvas73,game_window,canvas2x,GameState,a1,a2,a3,a4,messagebox,GameState,w1,w2,frame,menu,userx
    map_canvas=Canvas(root,width=1000,height=600,bg='black')
    map_canvas.pack()
    menu = xmenu
    frame = xframe
    game_window = root
    userx=user
    xframe.destroy()
    for i in range(0,20):
        map_canvas.create_line(50*i,0,50*i,700,fill='white')
    for j in range(0,14):
        map_canvas.create_line(0,50*j,1000,50*j,fill='white')
    for i in range(0,150):
        map_canvas.create_text(1000*random(),600*random(),fill='white',text='*')
    Marrow_room=map_canvas.create_rectangle(50,50,100,100,fill='brown')
    Gabriel_room=map_canvas.create_rectangle(200,200,300,300,fill='brown')
    Wolvingtom_room=map_canvas.create_rectangle(500,400,600,450,fill='brown')
    Overlord_room=map_canvas.create_rectangle(0,400,300,600,fill='brown')
    Shop=map_canvas.create_rectangle(800,400,1000,600,fill='#d3dd1f')
    Shop_Text=map_canvas.create_text(900,500,text='SHOP',fill='#777777',font=(None,40))
    t=Map(map_canvas,root)

def LoadMatchC(root,xframe,user,xmenu):
    global canvas73,game_window,canvas2x,GameState,a1,a2,a3,a4,messagebox,GameState,w1,w2,frame,menu,userx
    menu = xmenu
    frame = xframe
    game_window = root
    ChangeGameState(-40)
    w1 = Tank(player)
    w2 = Tank(player.boss)
    w2.colour = "brown"
    mainframe,canvas73 = LoadGame(game_window,frame,menu)

    w1.move(400)
    #canvas73.after(1000,lambda: LoadText1(1))
    canvas73.after(1000,LoadMatch2)

def LoadMatch2():
    w2.move(400)
    #canvas73.after(1000,lambda: LoadText1(4))
    canvas73.after(1000,LoadMatch3)

def LoadMatch3():
    global a1,a2,a3,a4,messagebox,GameState,game_window,canvas2x
    ChangeGameState(-1)
    t = canvas73.create_text(500,250,text=f"DEFEAT\n{w2}",fill="yellow",font=("showcard gothic",60))
    if found: ws.PlaySound(f'{w2}.wav', ws.SND_FILENAME | ws.SND_ASYNC)
    else: sp.Popen(['afplay',f'{w2}.wav'])
    canvas73.after(2000,lambda: canvas73.delete(t))
    canvas73.after(1500,lambda: SetGame(game_window,LoadMap))

def LoadText1(x,w=''):
    if x==1:
        w = canvas73.create_text(100,210,text="So silent this place is...",fill="#ffff00")
    elif x==2:
        canvas73.delete(w)
        w = canvas73.create_text(100,210,text="Those Zarixis must be terrified.",fill="#ffff00")
    elif x==3:
        canvas73.delete(w)
        LoadMatch2()
        return
    elif x==4:
        w = canvas73.create_text(250,210,text="",fill="#ffff00")
    elif x==5:
        canvas73.delete(w)
        w = canvas73.create_text(100,210,text="",fill="#ffff00")
    elif x==6:
        canvas73.delete(w)
        w = canvas73.create_text(250,210,text="",fill="#ffff00")
    elif x==7:
        canvas73.delete(w)
        w = canvas73.create_text(130,210,text="",fill="#ffff00")
    elif x==8:
        canvas73.delete(w)
        w = canvas73.create_text(250,210,text="",fill="#ffff00")
    elif x==9:
        canvas73.delete(w)
        LoadMatch3()
    elif x==10:
        w = canvas73.create_text(100,210,text="ENOUGH!",fill="#ffff00")
    elif x==11:
        canvas73.delete(w)
        return
    canvas73.after(3000,lambda: LoadText(x+1,w))