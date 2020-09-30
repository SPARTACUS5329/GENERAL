userDict={}
groupDict={}
class USERS:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.inbox_file=f"./UserfilesInbox/{self.username}.dat"
        self.outbox_file=f"./UserfilesOutbox/{self.username}.dat"
        self.toolbar_bg='light blue'
        self.side_frame_bg='bisque'
        self.body_frame_bg='light green'

class GROUP:
    def __init__(self,groupname,password,admin):
        self.groupname=groupname
        self.password=password
        self.chatfile=f"./Groups/{self.groupname}.dat"
        self.memberslist=[]
        self.admin=admin

SPARTACUS = USERS('SPARTACUS','c4a7f48fa54a')
userDict['SPARTACUS'] = SPARTACUS
Davie = USERS('Davie','ec32264f0b0x')
userDict['Davie'] = Davie


SPARTACUS.toolbar_bg = 'blue'
SPARTACUS.side_frame_bg = 'blue'
SPARTACUS.body_frame_bg = 'blue'
Divyam = USERS('Divyam','8c363fcdfe0f')
userDict['Divyam'] = Divyam
Divyam.toolbar_bg = 'light blue'
Divyam.side_frame_bg = 'light green'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'light blue'
Divyam.side_frame_bg = 'light green'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'light blue'
Divyam.side_frame_bg = 'light green'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'light blue'
Divyam.side_frame_bg = 'light green'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'bisque'
Divyam.side_frame_bg = 'yellow'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'bisque'
Divyam.side_frame_bg = 'yellow'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'bisque'
Divyam.side_frame_bg = 'green'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'bisque'
Divyam.side_frame_bg = 'yellow'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'bisque'
Divyam.side_frame_bg = 'green'
Divyam.body_frame_bg = 'light green'
Divyam.toolbar_bg = 'red'
Divyam.side_frame_bg = 'light green'
Divyam.body_frame_bg = 'bisque'
SPARTACUS.toolbar_bg = 'blue'
SPARTACUS.side_frame_bg = 'bisque'
SPARTACUS.body_frame_bg = 'light green'
SPARTACUS.toolbar_bg = 'bisque'
SPARTACUS.side_frame_bg = 'bisque'
SPARTACUS.body_frame_bg = 'bisque'
SPARTACUS.toolbar_bg = 'light green'
SPARTACUS.side_frame_bg = 'bisque'
SPARTACUS.body_frame_bg = 'green'