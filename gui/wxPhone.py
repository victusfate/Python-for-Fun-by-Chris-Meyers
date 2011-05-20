#   w x P h o n e . p y
#
from wxPython.wx import *
from phones  import *

class MyFrame (wxFrame) :
    def __init__ (self, parent, ID, title) :
        wxFrame.__init__(self, parent, ID, title, wxDefaultPosition, wxSize(300,325))
        wxStaticText(self,-1,"Name",wxDLG_PNT(self,15,5))
        self.name  = wxTextCtrl(self,12,"",wxDLG_PNT(self,40, 5),wxDLG_SZE(self,80,12))
        wxStaticText(self,-1,"Phone",wxDLG_PNT(self,15,25))
        self.phone = wxTextCtrl(self,12,"",wxDLG_PNT(self,40,25),wxDLG_SZE(self,80,12))

        b1 = wxButton(self,11,"Add",   wxDLG_PNT(self,10,45),wxDLG_SZE(self,25,12))
        b2 = wxButton(self,12,"Update",wxDLG_PNT(self,40,45),wxDLG_SZE(self,25,12))
        b3 = wxButton(self,13,"Delete",wxDLG_PNT(self,70,45),wxDLG_SZE(self,25,12))

        EVT_BUTTON(self, 11, self.addEntry)
        EVT_BUTTON(self, 12, self.updateEntry)
        EVT_BUTTON(self, 13, self.deleteEntry)

        self.lc = wxListCtrl(self,15,wxDLG_PNT(self,10,60),wxDLG_SZE(self,120,75),
                     style=wxLC_REPORT)
        self.lc.InsertColumn(0,"Name")
        self.lc.InsertColumn(1,"Phone")
        self.SetSize(self.GetSize())
        EVT_LIST_ITEM_SELECTED(self,15,self.getSelect)
    
    def setSelect (self) :
        phonelist.sort()
        self.lc.DeleteAllItems()
        for i in range(len(phonelist)) :
            name,phone = phonelist[i]
            self.lc.InsertStringItem(i, name)
            self.lc.SetStringItem(i, 1, phone)
        self.lc.SetColumnWidth(0, wxLIST_AUTOSIZE)
        self.currentSel = 0   # Just in case update attempted before load

    def getSelect (self, event) :
        self.currentSel = event.m_itemIndex
        name, phone = phonelist[self.currentSel]
        self.name.SetValue(name)
        self.phone.SetValue(phone)
        print "Selected", self.currentSel

    def addEntry (self, event) :
        phonelist.append ([self.name.GetValue(), self.phone.GetValue()])
        self.setSelect ()
    
    def updateEntry(self, event) :
        phonelist[self.currentSel] = [self.name.GetValue(), self.phone.GetValue()]
        self.setSelect ()
    
    def deleteEntry(self, event) :
        del phonelist[self.currentSel]
        self.setSelect ()
    
class MyApp (wxApp) :
    def OnInit (self) :
        frame = MyFrame(NULL, -1, "Phone List")
        frame.Show(true)
        frame.setSelect()
        self.SetTopWindow (frame)
        return true

def test () :
    app = MyApp(0)
    app.MainLoop()

