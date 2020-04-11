from . import _
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.config import config, configfile, ConfigSubsection, ConfigText, ConfigSelection, getConfigListEntry, ConfigYesNo, ConfigDirectory
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.FileList import FileList
from Components.Label import Label
from Components.Language import language
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists, pathExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE, SCOPE_MEDIA
from Tools.BoundFunction import boundFunction
from enigma import getDesktop, quitMainloop, eTimer
from os import popen
from IM_Console import IM_Console
from MountedDevs import Refresh, Activepart

skin_fhd_main = """
 <screen name="ImageManager" position="center,250" size="1100,500" title="Image Manager">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/icon/key_ok.png" position="60,340" size="40,20" zPosition="2" alphatest="on"/>
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/icon/key_info.png" position="60,370" size="40,20" zPosition="2" alphatest="on"/>
  <widget name="config" position="50,40" size="1000,200" transparent="1" alphatest="blend" itemHeight="30" font="Regular;25" scrollbarMode="showOnDemand" zPosition="2" foregroundColor="00f8ff50" backgroundColorSelected="#004EFF" foregroundColorSelected="#FFCC33"/>
  <widget render="Label" source="key_ok" position="120,335" size="400,30" transparent="1" zPosition="5" valign="center" halign="left" font="Regular;22"/>
  <widget render="Label" source="key_help" position="120,365" size="400,30" transparent="1" zPosition="5" valign="center" halign="left" font="Regular;22"/>
  <widget render="Label" source="activepart" position="640,335" size="400,65" transparent="1" zPosition="5" valign="center" halign="right" font="Regular;22"/>
  <eLabel position="50,330" size="1000,2" backgroundColor="#aaaaaa"/>
  <eLabel position="50,400" size="1000,2" backgroundColor="#aaaaaa"/>
  <eLabel position="50,40" size="1000,2" backgroundColor="#004EFF" transparent="0" zPosition="0" alphatest="blend"/>
  <eLabel position="50,68" size="1000,2" backgroundColor="#004EFF" transparent="0" zPosition="0" alphatest="blend"/>
 </screen>"""
skin_hd_main = """
 <screen name="ImageManager" position="center,130" size="850,360" >
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/icon/key_ok.png" position="60,240" size="40,20" zPosition="2" alphatest="on"/>
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/icon/key_info.png" position="60,270" size="40,20" zPosition="2" alphatest="on"/>
  <widget name="config" position="50,40" size="750,200" transparent="1" alphatest="blend" itemHeight="30" font="Regular;21" scrollbarMode="showOnDemand" zPosition="2" foregroundColor="00f8ff50" backgroundColorSelected="#004EFF" foregroundColorSelected="#FFCC33"/>
  <widget render="Label" source="key_ok" position="120,235" size="400,30" transparent="1" zPosition="5" valign="center" halign="left" font="Regular;18"/>
  <widget render="Label" source="key_help" position="120,265" size="400,30" transparent="1" zPosition="5" valign="center" halign="left" font="Regular;18"/>
  <widget render="Label" source="activepart" position="390,235" size="400,60" transparent="1" zPosition="5" valign="center" halign="right" font="Regular;18"/>
  <eLabel position="50,230" size="750,2" backgroundColor="#aaaaaa"/>
  <eLabel position="50,300" size="750,2" backgroundColor="#aaaaaa"/>
  <eLabel position="50,40" size="750,2" backgroundColor="#004EFF" transparent="0" zPosition="0" alphatest="blend"/>
  <eLabel position="50,68" size="750,2" backgroundColor="#004EFF" transparent="0" zPosition="0" alphatest="blend"/>
 </screen>"""
skin_sd_main = """
 <screen name="ImageManager" position="center,130" size="640,360" >
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/icon/key_ok.png" position="50,243" size="30,30" zPosition="2" alphatest="on"/>
  <widget name="config" position="40,40" size="560,200" transparent="1" alphatest="blend" itemHeight="30" font="Regular;21" scrollbarMode="showOnDemand" zPosition="2" foregroundColor="00f8ff50" backgroundColorSelected="#004EFF" foregroundColorSelected="#FFCC33"/>
  <widget render="Label" source="key_ok" position="90,240" size="100,30" transparent="1" zPosition="5" valign="center" halign="left" font="Regular;24"/>
  <widget render="Label" source="activepart" position="250,240" size="340,30" transparent="1" zPosition="5" valign="center" halign="right" font="Regular;18"/>
  <eLabel position="40,235" size="560,2" backgroundColor="#aaaaaa"/>
  <eLabel position="40,275" size="560,2" backgroundColor="#aaaaaa"/>
  <eLabel position="40,40" size="560,2" backgroundColor="#004EFF" transparent="0" zPosition="0" alphatest="blend"/>
  <eLabel position="40,68" size="560,2" backgroundColor="#004EFF" transparent="0" zPosition="0" alphatest="blend"/>
 </screen>"""

skin_fhd_filelist = """
  <screen position="center,center" size="1200,760">
    <widget name="filelist" position="20,20" size="1160,720" foregroundColor="#0000FF80" scrollbarMode="showOnDemand"/>
    <widget name="AboutScrollLabel" font="Regular;26" position="20,20" size="1160,720" foregroundColor="#0000FF80" scrollbarMode="showOnDemand"/>
  </screen>"""
skin_hd_filelist = """
  <screen position="center,center" size="700,560">
    <widget name="filelist" position="10,10" size="680,540" foregroundColor="#0000FF80" scrollbarMode="showOnDemand"/>
    <widget name="AboutScrollLabel" font="Regular;20" position="10,10" size="680,540" foregroundColor="#0000FF80" scrollbarMode="showOnDemand"/>
  </screen>"""
skin_sd_filelist = """
  <screen position="center,center" size="550,400">
    <widget name="filelist" position="10,10" size="530,380" foregroundColor="#0000FF80" scrollbarMode="showOnDemand"/>
    <widget name="AboutScrollLabel" font="Regular;20" position="10,10" size="530,380" foregroundColor="#0000FF80" scrollbarMode="showOnDemand"/>
  </screen>""" 

Refresh('check')    
f = open('/proc/stb/info/model', 'r')
model = f.readline().strip()
f.close()
#model = "spark"
BIN = '/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/bin/'
pluginversion = '2.7' 
screenWidth = getDesktop(0).size().width()
config.plugins.ImageManager = ConfigSubsection()
config.plugins.ImageManager.startmode = ConfigSelection(default='mboot', choices=[('mboot', _('Multiboot')),
 ('backup', _('Backup')),
 ('copy', _('Copying')),
 ('rename', _('Rename')),
 ('install', _('Installing'))])
config.plugins.ImageManager.showext = ConfigYesNo(default=False)
config.plugins.ImageManager.sparkrebootext = ConfigYesNo(default=False)
config.plugins.ImageManager.sparkrebootshutdown = ConfigYesNo(default=False)
config.plugins.ImageManager.mode = ConfigSelection(choices=[('mboot', _('Multiboot')),
 ('backup', _('Backup')),
 ('copy', _('Copying')),
 ('rename', _('Rename')),
 ('install', _('Installing')),
 ('cfgmenu', _('Configuration'))])
config.plugins.ImageManager.installmode = ConfigSelection(default='repack', choices=[('repack', _('repacking')), ('mounting', _('mounting'))])

class ImageManager(ConfigListScreen, Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        if screenWidth and screenWidth == 1920:
            self.skin = skin_fhd_main
        elif screenWidth and screenWidth == 1280:
            self.skin = skin_hd_main
        else:
            self.skin = skin_sd_main 
        config.plugins.ImageManager.mode.value = config.plugins.ImageManager.startmode.value
        config.plugins.ImageManager.newName = ConfigText(visible_width=16, fixed_size=True)
        config.plugins.ImageManager.imagetype = ConfigSelection(default=_('no'), choices=[('YES', _('yes')), ('NO', _('no'))])
        config.plugins.ImageManager.archivetype = ConfigSelection(default='IMG', choices=[('IMG', 'IMG'),
         ('TAR', 'TAR'), ('TARGZ', 'TAR.GZ'), ('TARBZIP', 'TAR.BZIP')])
        config.plugins.ImageManager.emu = ConfigSelection(default='XXX', choices=[('WMO', 'Wicardd, MgCamd, Oscam'),
         ('WM', 'Wicardd, MgCamd'), ('WO', 'Wicardd, Oscam'),
         ('MO', 'MgCamd, Oscam'), ('O', 'Oscam'),
         ('W', 'Wicardd'), ('M', 'MgCamd'), ('XXX', _('no'))]) 
        Refresh('job')
        self.setTitle(_('Image Manager ver %s (c)Vasiliks') % pluginversion)
        self['key_ok'] = Label(_('Execute'))
        self['key_help'] = Label(_('Help'))
        self['activepart'] = Label(_('Active Partition  -  ') + Activepart())
        self['myActionMap'] = ActionMap(['OkCancelActions', 'ColorActions', 'StandbyActions', 'EPGSelectActions'], {
         'ok': self.Execute,
         'cancel': self.cancel,
         'info': self.keyHelp, 
         'green': self.Execute,  
         'red': self.cancel, 
         'power': self.reboot_spark
        }, -2)
        self.list = [ ]
        ConfigListScreen.__init__(self, self.list, session=session)
        self.createConfigList()  

    def createConfigList(self):
        self.list = [ ]
        self.mode = getConfigListEntry(_('Select Mode:'), config.plugins.ImageManager.mode)
        self.list.append(self.mode)
        if config.plugins.ImageManager.mode.value == 'backup':
            self.list.extend((getConfigListEntry(_('Select the source partition:'), config.plugins.ImageManager.devsFrom),
             getConfigListEntry(_('Select the target partition:'), config.plugins.ImageManager.devsToBackup),
             getConfigListEntry(_('Select the type of archive:'), config.plugins.ImageManager.archivetype),
             getConfigListEntry(_('Delete the configuration file Enigma?'), config.plugins.ImageManager.imagetype),
             getConfigListEntry(_('Remove config settings EMU?'), config.plugins.ImageManager.emu)))
        if config.plugins.ImageManager.mode.value == 'cfgmenu':
            self.list.extend((getConfigListEntry(_('Mode at startup:'), config.plugins.ImageManager.startmode),
             getConfigListEntry(_('Show ImageManager in ExtensionsMenu?'), config.plugins.ImageManager.showext),
             getConfigListEntry(_('Show Reboot to Spark in ExtensionsMenu?'), config.plugins.ImageManager.sparkrebootext),
             getConfigListEntry(_('Show Reboot to Spark in ShutdownMenu?'), config.plugins.ImageManager.sparkrebootshutdown)))
        if config.plugins.ImageManager.mode.value == 'copy':
            config.plugins.ImageManager.newName.value = 'NewName_For_Copy'
            self.list.extend((getConfigListEntry(_('Select the source partition:'), config.plugins.ImageManager.devsFrom),
             getConfigListEntry(_('Select the target partition:'), config.plugins.ImageManager.devsToCopy),
             getConfigListEntry(_('Input name:'), config.plugins.ImageManager.newName),
             getConfigListEntry(_('Delete the configuration file Enigma?'), config.plugins.ImageManager.imagetype)))
        if config.plugins.ImageManager.mode.value == 'install':
            self.list.append(getConfigListEntry(_('Select the target partition:'), config.plugins.ImageManager.devsToCopy))
            self.list.append(getConfigListEntry(_('Select install mode:'), config.plugins.ImageManager.installmode))
        if config.plugins.ImageManager.mode.value == 'mboot':
            self.list.append(getConfigListEntry(_('Select the source partition:'), config.plugins.ImageManager.devsFrom))
        if config.plugins.ImageManager.mode.value == 'rename':
            config.plugins.ImageManager.newName.value = 'NewNamePartition'
            self.list.append(getConfigListEntry(_('Select the partition to rename:'), config.plugins.ImageManager.devsToCopy))
            self.list.append(getConfigListEntry(_('Input name:'), config.plugins.ImageManager.newName))
        self["config"].setList(self.list)

    def newConfig(self):
        if self["config"].getCurrent() == self.mode:
            self.createConfigList()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.newConfig()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.newConfig()
        
    def keyHelp(self):
        self.session.open(ImageManagerHelp)

    def Execute(self):
        if config.plugins.ImageManager.mode.value == 'mboot':
            devBoot = config.plugins.ImageManager.devsFrom.value[config.plugins.ImageManager.devsFrom.value.find('/dev/'):]
            self.reBootAll(devBoot)
        elif config.plugins.ImageManager.mode.value == 'backup':
            self.makeBackup = BIN + 'backup.sh'
            self.makeBackup += ' %s %s %s %s %s' % (config.plugins.ImageManager.devsFrom.value, config.plugins.ImageManager.devsToBackup.value,
             config.plugins.ImageManager.archivetype.value, config.plugins.ImageManager.imagetype.value, config.plugins.ImageManager.emu.value)
            self.session.open(IM_Console, _('Backup Creator'), ['%s' % self.makeBackup])
        elif config.plugins.ImageManager.mode.value == 'copy':
            self.copying()  
        elif config.plugins.ImageManager.mode.value == 'install':
            self.session.openWithCallback(self.createConfigList, Install_IM)
        elif config.plugins.ImageManager.mode.value == 'rename':
            renamepart = config.plugins.ImageManager.devsToCopy.value[config.plugins.ImageManager.devsToCopy.value.find('/dev/'):]
            popen("umount -l %s" % (renamepart))
            popen("tune2fs -L %s %s" % (config.plugins.ImageManager.newName.value, renamepart))
            Refresh('job')
            newname = _('Partition %s\nrenamed in %s') % (renamepart, config.plugins.ImageManager.newName.value)
            self.session.open(MessageBox, newname, type=MessageBox.TYPE_INFO, timeout=5)
            self.createConfigList()
        elif config.plugins.ImageManager.mode.value == 'cfgmenu':
            config.plugins.ImageManager.startmode.save()
            config.plugins.ImageManager.sparkrebootext.save()
            config.plugins.ImageManager.sparkrebootshutdown.save()
            config.plugins.ImageManager.showext.save()
            configfile.save()
            self.session.open(MessageBox, _('Configuration is saved'), MessageBox.TYPE_INFO, timeout=4)
            from Components.PluginComponent import plugins
            plugins.reloadPlugins()
        else:
            self.close()
        
    def cancel(self):
        popen('rm /tmp/blkid.*')
        self.close()
        
    def copying(self):
        self.makeCopy = BIN + 'copying.sh'
        self.makeCopy += ' %s %s %s %s' % (config.plugins.ImageManager.devsFrom.value,
         config.plugins.ImageManager.devsToCopy.value,
         config.plugins.ImageManager.imagetype.value,
         config.plugins.ImageManager.newName.value)
        self.session.openWithCallback(self.end_copy, IM_Console, _('Copying of partition'), ['%s' % self.makeCopy])

    def end_copy(self):     
        Refresh('job')
        self.createConfigList()

    def reboot_spark(self):
        self.reBootAll('SPARK')

    def reBootAll(self, devBoot):
        print 'ImageManager fuond - ', model
        if model == 'spark':
            MBoot = BIN + 'setIMG.sh'
        elif model == 'spark7162':
            MBoot = BIN + 'setIMG7162.sh'
        else:
            return
        self.session.nav.stopService()
        parametr = ' NAND'
        if devBoot == 'SPARK':
            parametr = ' SPARK'
        elif devBoot != '/dev/mtdblock6':
            parametr = ' USB ' + devBoot
        popen(MBoot + parametr)
        if fileExists('/tmp/mboot.log'):
            file = open('/tmp/mboot.log', 'r')
            lines = file.readlines()
            file.close()
            self.session.open(MessageBox, ''.join(lines), type=MessageBox.TYPE_INFO, timeout=10)
        if fileExists('/tmp/mboot.ok'):
            quitMainloop(2)
        elif fileExists('/tmp/mboot.error'):
            pass
        else:
            self.session.open(MessageBox, 'Unknown error occured :(', type=MessageBox.TYPE_INFO, timeout=5)

class Install_IM(Screen):
    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        if screenWidth and screenWidth == 1920:
            self.skin = skin_fhd_filelist
        elif screenWidth and screenWidth == 1280:
            self.skin = skin_hd_filelist
        else:
            self.skin = skin_sd_filelist
        self.setTitle(_('Select the image'))
        self.session = session
        hide = ['/bin', '/boot', '/dev', '/dev.static', '/etc', '/lib',
         '/proc', '/ram', '/root', '/sbin', '/sys', '/tmp', '/usr', '/var']
        extensions='(?i)^.*\\.(img|tar|gz|bz2)'
        self['filelist'] = FileList(ConfigDirectory().getValue(), showMountpoints=True, matchingPattern=extensions, inhibitDirs=hide)
        self['actions'] = ActionMap(['WizardActions'], {'ok': self.ok, 'back': self.back, 'up': self.up,
         'down': self.down, 'left': self.left, 'right': self.right}, -1)

    def back(self):
        self.close()

    def up(self):
        self['filelist'].up()

    def down(self):
        self['filelist'].down()

    def left(self):
        self['filelist'].pageUp()

    def right(self):
        self['filelist'].pageDown()

    def ok(self):
        if self['filelist'].canDescent():
            self['filelist'].descent()
        elif self['filelist'].getFilename() != None:
            self.title = _('Image Installer')
            target = config.plugins.ImageManager.devsToCopy.value[config.plugins.ImageManager.devsToCopy.value.find('/dev/'):]
            namepart = self["filelist"].getCurrentDirectory()[:self["filelist"].getCurrentDirectory().rfind('/')]
            namepart = namepart[namepart.rfind('/') + 1:] 
            self.script = BIN + 'install.sh'
            self.script += ' %s %s %s %s %s' % (target, self['filelist'].getCurrentDirectory(), self['filelist'].getFilename(), namepart, config.plugins.ImageManager.installmode.value)
            message = _('Do you want to install with this image?\n%s\nto partition %s') % (self['filelist'].getCurrentDirectory() + self['filelist'].getFilename(), target)
            self.session.openWithCallback(self.Execution, MessageBox, message, timeout=0, default=True)

    def Execution(self, answer):
        if answer:
            self.session.openWithCallback(self.cancel, IM_Console, self.title, ['%s' % self.script])

    def cancel(self):
        Refresh('job')
        self.close()

class ImageManagerHelp(Screen):
    def __init__(self, session):
        if screenWidth and screenWidth == 1920:
            self.skin = skin_fhd_filelist
        elif screenWidth and screenWidth == 1280:
            self.skin = skin_hd_filelist
        else:
            self.skin = skin_sd_filelist

        Screen.__init__(self, session)
        self["Title"].setText(_("Short Help"))
        self["AboutScrollLabel"] = ScrollLabel(_(""))
        self["actions"] = ActionMap(["SetupActions", "DirectionActions"],
            {
                "cancel": self.close,
                "ok": self.close,
                "up": self["AboutScrollLabel"].pageUp,
                "down": self["AboutScrollLabel"].pageDown
            })
        with open('/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/imagemanager.hlp') as file_help:
            help_im = file_help.read()
        self["AboutScrollLabel"].setText(help_im)

class Dialog(Screen):

    skin = """
           <screen  position="50,40" size="120,30" zPosition="-1" backgroundColor="#ff000000" flags="wfNoBorder">
           </screen>"""
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.skinName = Dialog.skin
        self.timer = eTimer()
        self.timer.callback.append(self.update)
        self.timer.start(600, True)
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.ok,
         'cancel': self.exit}, -1)

    def ok(self):
        self.close()

    def exit(self):
        self.close()                                    

    def update(self):        
        if model != 'spark' and model != 'spark7162':
            self.session.openWithCallback(self.workingFinished, MessageBox, _('Unknown box! :( :( :('), type=MessageBox.TYPE_INFO, timeout=30)
        elif Refresh('check'):
            message = _('Not found USB-Flash! :( :( :(\nStart plugin without USB-Flash?')
            self.session.openWithCallback(self.start2, MessageBox, message, MessageBox.TYPE_YESNO)
        else:
            self.session.openWithCallback(self.workingFinished, ImageManager)

    def workingFinished(self, callback = None):
        self.close()

    def start2(self, answer):
        if answer:
            self.session.openWithCallback(self.workingFinished, ImageManager)
        else:
            self.close()
        
def start(session, **kwargs):
    session.open(Dialog)
        
def spark(session, **kwargs):
    SparkReboot = ImageManager(session)
    SparkReboot.reboot_spark()
                              
def menu(menuid):
    if menuid == 'shutdown':
        return [(_('Reboot to Spark'), spark, 'reboot_to_spark', None)]
    else:
        return []

def Plugins(**kwargs):
    list = [PluginDescriptor(name=_('Image Manager'), description=_('manage of your image Enigma'), where=[PluginDescriptor.WHERE_PLUGINMENU], icon='icon/ImageManager.png', fnc=start)]
    if config.plugins.ImageManager.showext.value:
        list.append(PluginDescriptor(name=_('Image Manager'), description=_('manage of your image Enigma'), where=[PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=start))
    if config.plugins.ImageManager.sparkrebootshutdown.value:
        list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_MENU], fnc=menu))
    if config.plugins.ImageManager.sparkrebootext.value:
        list.append(PluginDescriptor(name=_('Reboot to Spark'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=spark))
    return list
