from enigma import addFont, eConsoleAppContainer, getDesktop
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel

try:
    addFont("/usr/share/fonts/valis_enigma.ttf", "ConsoleIM", 100, 1)
except Exception as ex:
    print ex  
         
class IM_Console(Screen):
    screenWidth = getDesktop(0).size().width()
    if screenWidth and screenWidth == 1920:
        skin = """
            <screen position="center,center" size="1200,760" title="Command execution...">
                <widget name="text" position="40,40" size="1100,720" font="ConsoleIM;24"/>
            </screen>"""
    elif screenWidth and screenWidth == 1280:
        skin = """
            <screen position="center,center" size="850,540" title="Command execution...">                         
                <widget name="text" position="50,40" size="750,460" font="ConsoleIM;20" />
            </screen>"""
    else:
        skin = """ 
            <screen position="center,center" size="640,360" title="Command execution...">
                <widget name="text" position="40,40" size="560,280"font="ConsoleIM;18" />
            </screen>"""
    def __init__(self, session, title = "ImageManager_Console", cmdlist = None, finishedCallback = None, closeOnSuccess = False):
        Screen.__init__(self, session)
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.errorOcurred = False
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions'],
         {'ok': self.cancel, 'back': self.cancel,
          'up': self['text'].pageUp, 'down': self['text'].pageDown}, -1)
        self.cmdlist = cmdlist
        self.newtitle = title
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run = 0
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        self['text'].setText(_('Execution progress:') + '\n\n')
        print 'Console: executing in run', self.run, ' the command:', self.cmdlist[self.run]
        if self.container.execute(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        if retval:
            self.errorOcurred = True
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            lastpage = self['text'].isAtLastPage()
            str = self['text'].getText()
            str += _('Execution finished!!')
            self['text'].setText(str)
            if lastpage:
                self['text'].lastPage()
            if self.finishedCallback is not None:
                self.finishedCallback()
            if not self.errorOcurred and self.closeOnSuccess:
                self.cancel()

    def cancel(self):
        if self.run == len(self.cmdlist):
            self.close()
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)

    def dataAvail(self, str):
        lastpage = self['text'].isAtLastPage()
        self['text'].setText(self['text'].getText() + str)
        if lastpage:
            self['text'].lastPage()
