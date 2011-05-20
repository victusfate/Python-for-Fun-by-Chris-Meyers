#   s q l P h o n e . p y
#
#    Maintain mysql database table 'phones'
#
from Tkinter import *
import MySQL
db = MySQL.connect('')
db.selectdb("test")

def whichSelected () :
    print "At %s" % (select.curselection())
    return int(select.curselection()[0])

def dosql (cmd) :
    print cmd
    c = db.query(cmd)
    setSelect ()

def addEntry () :
    c = db.query("select max(id)+1 from phones")
    id = c.fetchdict()[0].values()[0]  # digs deep to get next id
    dosql("insert into phones values (%d,'%s','%s')" % (id,nameVar.get(), phoneVar.get()))

def updateEntry() :
    id = phoneList[whichSelected()][0]
    dosql("update phones set name='%s', phone='%s' where id=%d" %
                   (nameVar.get(), phoneVar.get(), id))

def deleteEntry() :
    id = phoneList[whichSelected()][0]
    dosql("delete from phones where id=%d" % id)

def loadEntry  () :
    id, name, phone = phoneList[whichSelected()]
    nameVar.set(name)
    phoneVar.set(phone)

def makeWindow () :
    global nameVar, phoneVar, select
    win = Tk()

    frame1 = Frame(win)
    frame1.pack()

    Label(frame1, text="Name").grid(row=0, column=0, sticky=W)
    nameVar = StringVar()
    name = Entry(frame1, textvariable=nameVar)
    name.grid(row=0, column=1, sticky=W)

    Label(frame1, text="Phone").grid(row=1, column=0, sticky=W)
    phoneVar= StringVar()
    phone= Entry(frame1, textvariable=phoneVar)
    phone.grid(row=1, column=1, sticky=W)

    frame2 = Frame(win)       # Row of buttons
    frame2.pack()
    b1 = Button(frame2,text=" Add  ",command=addEntry)
    b2 = Button(frame2,text="Update",command=updateEntry)
    b3 = Button(frame2,text="Delete",command=deleteEntry)
    b4 = Button(frame2,text="Load  ",command=loadEntry)
    b5 = Button(frame2,text="Refresh",command=setSelect)
    b1.pack(side=LEFT); b2.pack(side=LEFT)
    b3.pack(side=LEFT); b4.pack(side=LEFT); b5.pack(side=LEFT)

    frame3 = Frame(win)       # select of names
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=6)
    scroll.config (command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)
    return win

def setSelect () :
    global phoneList
    c = db.query("select id,name,phone from phones order by name")
    phoneList = c.fetchrows()
    select.delete(0,END)
    for id,name,phone in phoneList :
        select.insert (END, name)

win = makeWindow()
setSelect ()
win.mainloop()


