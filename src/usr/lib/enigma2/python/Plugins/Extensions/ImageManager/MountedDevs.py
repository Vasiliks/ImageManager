from Components.config import config, ConfigSelection
from os import popen

def getMountedDevs(aaa):
    mountedDevs = []
    if aaa & 1:
        a=open("/tmp/blkid.im", "r")
        for b in a.readlines():
            DevList = b.strip('\n').replace('\\040', ' ')
            if DevList.find("vfat") > -1:
                if DevList.find('LABEL') > -1:
                    NAME = DevList[DevList.find('LABEL="')+7:]
                    NAME = NAME[:NAME.find('"')]
                else:
                    NAME = 'noNAME'
                SDXY = DevList.split(":",1)[0]
                mountedDevs.append((NAME+' '+SDXY, NAME+' ( '+SDXY+' )'))
        a.close()
        a=open("/proc/mounts", "r")
        for b in a.readlines():
            DevList = b.strip('\n').replace('\\040', ' ')
            if DevList.find('/media/net/') > -1:
                NAMEshort = DevList[DevList.find('/media/')+11:]
                NAMEshort = NAMEshort[:NAMEshort.find(' ')]
                NAMEfull = DevList[DevList.find('/media/'):]
                NAMEfull = NAMEfull[:NAMEfull.find(' ')]
                SDXY = DevList[:DevList.find(' ')]
                mountedDevs.append((NAMEfull+' '+NAMEfull, NAMEshort+' ( '+SDXY+' )'))
        a.close()
    if aaa & 2:
        mountedDevs.append(('NAND /dev/mtdblock6', 'NAND-Flash'))
    if aaa & 4:
        a=open("/tmp/blkid.im", "r")
        for b in a.readlines():
            DevList = b.strip('\n')
            if DevList.find('TYPE="ext') > 0:
                SDXY = DevList.split(":",1)[0]
                if DevList.find('LABEL="') > 0:
                    NAME = DevList[DevList.find('LABEL="')+7:]
                    NAME = NAME[:NAME.find('"')]
                else:
                    NAME = SDXY[5:].upper()
                if aaa & 2 or SDXY != Activepart():
                    mountedDevs.append((NAME+' '+SDXY, NAME+' ( '+SDXY+' )'))
        a.close()
    return mountedDevs

def Activepart():
    f = open("/proc/cmdline", "r")
    b = f.readline()
    f.close()
    c = b.strip('\n')
    a = c[c.find('/dev/'):]
    a = a[:a.find(' ')]
    if a == "/dev/mtdblock6":
        a = _("NAND-Flash")
    return a

def Refresh(mode):
    popen('echo 3 > /proc/sys/vm/drop_caches && blkid > /tmp/blkid.tmp')
    if mode == 'check':
        no_hdd=True
        items=open("/tmp/blkid.tmp", "r")
        for item in items.readlines():
            if item.__contains__('TYPE="ext') or item.__contains__('TYPE="vfat'):
                no_hdd=False
                break
        items.close()
        return no_hdd
    elif mode == 'job':
        f_out = open('/tmp/blkid.im', "w")
        f_in = open('/tmp/blkid.tmp', "r")
        blkid_tmp = f_in.readlines()
        f_in.close()
        for sd in 'a', 'b':
            for i in xrange(1, 15):
                for j in blkid_tmp:
                    if j.__contains__('sd%s%d:' % (sd, i)):
                        blkid_tmp.remove(j)
                        p = j[j.find('UUID="'):]
                        j = j.replace(p[:p.find(' ')+1], '')
                        f_out.write(j)
        f_out.close()
        config.plugins.ImageManager.devsFrom = ConfigSelection(choices=getMountedDevs(6))
        config.plugins.ImageManager.devsToBackup = ConfigSelection(choices=getMountedDevs(5))
        config.plugins.ImageManager.devsToCopy = ConfigSelection(choices=getMountedDevs(4))
