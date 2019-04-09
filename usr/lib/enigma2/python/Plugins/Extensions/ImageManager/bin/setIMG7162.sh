#!/bin/sh
#Lexandros 03.2015 (thanks for j00zek and  Vasiliks)
LOG(){
echo "$1"
echo "$1" >>/tmp/mboot.log
echo "$1" >/hdd/MBoot.log
}

GOTERROR(){
echo "$1"
echo "$1" >>/tmp/mboot.log
echo "$1" >/hdd/MBoot.log
touch /tmp/mboot.error
exit 1
}
[ -f /tmp/fw_env.config ] && rm -rf /tmp/fw_env.config
[ -f /tmp/mboot.ok ] && rm -rf /tmp/mboot.ok
[ -f /tmp/mboot.error ] && rm -rf /tmp/mboot.error
[ -f /tmp/mboot.log ] && rm -rf /tmp/mboot.log
[ -f $BIN/fw_printenv ] && rm -rf $BIN/fw_printenv
echo "##### setIMG.sh `date` #####" >/hdd/MBoot.log
# checking box type
BIN="/usr/lib/enigma2/python/Plugins/Extensions/ImageManager/bin"
LOG "spark7162 detected :)"
[ -e /tmp/fw_env.config ] || ln -sf $BIN/fw_env.config.spark7162 /tmp/fw_env.config
[ -e $BIN/fw_printenv ] || ln -sf $BIN/fw_setenv $BIN/fw_printenv

if [ $1 == "SPARK" ]; then
################## REBOOT TO SPARK ###############################
	bootargs_spark='console=ttyAS1,115200 rw ramdisk_size=6144 init=/linuxrc root=/dev/ram0 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:69 ip=192.168.0.69:192.168.3.119:192.168.3.1:255.255.0.0:Spark:eth0:off stmmaceth=msglvl:0,phyaddr:1,watchdog:5000 bigphysarea=7000'
	userfs_base_spark="0x01400000"
	userfs_len_spark="0x16c00000"
	kernel_base_spark="0x00100000"
	bootcmd_spark="nboot.i 0x80000000 0  0x00100000 ;bootm 0x80000000"

	if `cat /proc/mtd | grep -q 'mtd7:'`; then
		LOG "spark7162, i2s.ko module already loaded"
	else
		if [ -e /lib/modules/i2s.ko ]; then
			insmod /lib/modules/i2s.ko
			[ $? -gt 0 ] && GOTERROR "error inserting i2s module"
		else
			VERSMODULES=`ls /lib/modules |grep "2.6.32"`
			PATHMODULES=/lib/modules/$VERSMODULES/extra/i2c_spi
			if [ -e $PATHMODULES/i2s.ko ]; then
				insmod $PATHMODULES/i2s.ko
			[ $? -gt 0 ] && GOTERROR "error inserting i2s module"
			fi
		fi
		
		if `cat /proc/mtd | grep -q 'mtd7:'`; then
			LOG "spark7162, i2s.ko module loaded successfull"
		else 
			GOTERROR "error inserting i2s module"
		fi
	fi



echo "Writing bootargs..."
#bootargs
$BIN/fw_setenv bootargs "$bootargs_spark"
[ $? -gt 0 ] && GOTERROR "error writing bootargs" || LOG "bootargs configured"
#bootcmd
$BIN/fw_setenv bootcmd "$bootcmd_spark"
[ $? -gt 0 ] && GOTERROR "error writing bootcmd" || LOG "bootcmd configured"
#userfs_base_spark
$BIN/fw_setenv userfs_base "$userfs_base_spark"
[ $? -gt 0 ] && GOTERROR "error writing userfs_base" || LOG "userfs_base configured"
#userfs_len_spark
$BIN/fw_setenv userfs_len "$userfs_len_spark"
[ $? -gt 0 ] && GOTERROR "error writing userfs_len" || LOG "userfs_len configured"
#kernel_base_spark
$BIN/fw_setenv kernel_base "$kernel_base_spark"
[ $? -gt 0 ] && GOTERROR "error writing kernel_base" || LOG "kernel_base configured"
#taki sam dla obu sparkow
$BIN/fw_setenv kernel_name "spark/mImage"
[ $? -gt 0 ] && GOTERROR "error writing kernel_name" || LOG "kernel_name configured"
#taki sam dla obu sparkow
$BIN/fw_setenv userfs_name "spark/userfsub.img"
[ $? -gt 0 ] && GOTERROR "error writing userfs_name" || LOG "userfs_name configured"
#taki sam dla obu sparkow
$BIN/fw_setenv tftp_kernel_name "mImage"
[ $? -gt 0 ] && GOTERROR "error writing tftp_kernel_name" || LOG "tftp_kernel_name configured"
#taki sam dla obu sparkow
$BIN/fw_setenv tftp_userfs_name "userfsub.img"
[ $? -gt 0 ] && GOTERROR "error writing tftp_userfs_name" || LOG "tftp_userfs_name configured"
#taki sam dla obu sparkow
$BIN/fw_setenv boot_system "spark"
[ $? -gt 0 ] && GOTERROR "error writing boot_system" || LOG "boot_system configured"

else
################## REBOOT FROM USB ###############################
#checking parameters
if [ -z $1 ]; then
    GOTERROR "usage: setIMG.sh [NAND|USB sd[abcd][1-9]]"
else
    if  [ -z $2 ]; then
    if ! [ $1 == "NAND" ]; then
        GOTERROR "For boot from USB use: setIMG.sh USB sd[abcd][1-9]"
    fi
    fi
fi

sdXY=`echo $2 | sed "s;/dev/;;"`
echo "Active partition: '$sdXY'"
# do we realy need to change anything?
if `cat /proc/cmdline | grep -q "/dev/$sdXY"`; then
    if `echo $1 | grep -q 'USB'`; then
        LOG "Restart current soft from $sdXY"
        touch /tmp/mboot.ok
        sync
        exit 0
    fi
fi
if `cat /proc/cmdline | grep -q '/dev/mtdblock6'`; then
    if `echo $1 | grep -q 'NAND'`; then
        LOG "Restart current soft from NAND"
        touch /tmp/mboot.ok
        sync
        exit 0
    fi
fi

    	MyBootCMD="nboot.i 0x80000000 0  0x18000000 ;bootm 0x80000000"
	MyBootARGS=""
	MyMBoot_bootcmd='nboot.i 80000000 0 18400000;run MBoot_bootargs;bootm 80000000;set bootargs ${bootargs_enigma2};nboot.i 80000000 0 18000000;bootm 80000000'
	MyMBoot_bootargs='setenv bootargs "console=ttyAS0,115200 rw root=/dev/'$sdXY' init=/bin/devinit coprocessor_mem=4m@0x40000000,4m@0x40400000 printk=1 nwhwconf=device:eth0,hwaddr:00:80:E1:12:40:61 ip=172.100.100.249:172.100.100.174:172.100.100.174:${netmask}:Enigma2:eth0:off stmmaceth=msglvl:0,phyaddr:2,watchdog:5000 bigphysarea=6000 rootdelay=9"'
	[ -e /tmp/fw_env.config ] || ln -sf $BIN/fw_env.config.spark7162 /tmp/fw_env.config

	if `cat /proc/mtd | grep -q 'mtd7:'`; then
		LOG "spark7162, i2s.ko module already loaded"
	else
		if [ -e /lib/modules/i2s.ko ]; then
			insmod /lib/modules/i2s.ko
			[ $? -gt 0 ] && GOTERROR "error inserting i2s module"
		else
			VERSMODULES=`ls /lib/modules |grep "2.6.32"`
			PATHMODULES=/lib/modules/$VERSMODULES/extra/i2c_spi
			if [ -e $PATHMODULES/i2s.ko ]; then
				insmod $PATHMODULES/i2s.ko
			[ $? -gt 0 ] && GOTERROR "error inserting i2s module"
			fi
		fi
		
		if `cat /proc/mtd | grep -q 'mtd7:'`; then
			LOG "spark7162, i2s.ko module loaded successfull"
		else 
			GOTERROR "error inserting i2s module"
		fi
	fi

if `echo $1 | grep -q 'USB'`; then
    if ! `echo $2 | grep -q 'sd[abcd][1-9]'`; then
        GOTERROR "Error, got incorrect parameter :( ($1)"
        exit 1
    fi
	
	
	

    MBoot_bootargs=$MyMBoot_bootargs
    MBoot_bootcmd=$MyMBoot_bootcmd
# mounting partition & unmouting partition if already mounted
    if `mount | grep '/tmp/MBOOT' | grep -q /dev/$sdXY`; then
        LOG "unmounting /tmp/MBOOT folder"
        umount -l /tmp/MBOOT 2>/dev/null
    fi
    if `mount | grep '/tmp/MBOOT' | grep -q /dev/$sdXY`; then
        GOTERROR "ERROR, partition cannot be unmounted :("
        exit 1
    fi
# if there is no our catalog, it is necessary to create
    if [ ! -d /tmp/MBOOT ]; then
        LOG "Creating /tmp/MBOOT folder"
        mkdir /tmp/MBOOT
    fi
# if we partition is unmounted, let's check the consistency
    if ! `mount | grep -q /dev/$sdXY`; then
        LOG "checking partition consistency"
        e2fsck -p /dev/$sdXY
    fi
# mounting a suitable partition
    LOG "mounting partition"
    mount /dev/$sdXY /tmp/MBOOT
    if ! `mount | grep -q /dev/$sdXY`; then
        GOTERROR "ERROR: Mount partitions, finish work"
        exit 1
    fi
    if [ ! -e /tmp/MBOOT/boot/uImage ]; then
        GOTERROR "ERROR: Mounted partition contains the / boot / uImage. I finish work!!!"
        exit 1
    fi
# some improvements
    sed -i "s/\$1\$K\$Oy86o0YspthTr2IXvUm751//" /tmp/MBOOT/etc/passwd
# programming 2nd kernel
    LOG "Erasing 2nd kernel space in flash..."
    echo "ErASE nAnd.." >/dev/vfd
    flash_erase /dev/mtd5 0x400000 0x20
    [ $? -gt 0 ] && GOTERROR "error erasing nand"

    LOG "Writing 2nd kernel to NAND..."
    echo "FLASH 2nd kernel to nAnd.." >/dev/vfd
    nandwrite -s 0x400000 -p /dev/mtd5 /tmp/MBOOT/boot/uImage
    [ $? -gt 0 ] && GOTERROR "error writing nand"
else # boot from NAND
    MBoot_bootargs=$MyBootARGS
    MBoot_bootcmd=$MyBootCMD
fi
# checking environment
[ -e $BIN/fw_printenv ] || ln -sf $BIN/fw_setenv $BIN/fw_printenv
myENV=`$BIN/fw_printenv`
RET=$?
if [ $RET -eq 0 ]; then
    LOG "Valid fw_env detected :)"
else
    GOTERROR "fw_env misconfigured :("
fi

LOG "Writing bootargs..."
# MBoot_bootargs
$BIN/fw_setenv MBoot_bootargs "$MBoot_bootargs"
[ $? -gt 0 ] && GOTERROR "error writing MBoot_bootargs"

# MBoot_bootcmd
$BIN/fw_setenv bootcmd "$MBoot_bootcmd"
[ $? -gt 0 ] && GOTERROR "error writing MBoot_bootcmd"

# To check if all required written correctly
myENV=`$BIN/fw_printenv`
if ! `echo $myENV | grep -q "bootcmd="`;then
    [ $? -gt 0 ] && GOTERROR "error no bootcmd found after flashing"
fi
if ! `echo $myENV | grep -q "bootargs="`;then
    $BIN/fw_setenv MBoot_ON
    [ $? -gt 0 ] && GOTERROR "error no bootargs found after flashing"
fi

# cleaning trashes
LOG "cleaning up..."
if `echo $myENV | grep -q "MBoot_ON"`;then
    $BIN/fw_setenv MBoot_ON
    [ $? -gt 0 ] && GOTERROR "error removing MBoot_ON"
fi
if `echo $myENV | grep -q "MBoot_sda_NO"`;then
    $BIN/fw_setenv MBoot_sda_NO
    [ $? -gt 0 ] && GOTERROR "error removing MBoot_sda_NO"
fi
if `echo $myENV | grep -q "MBoot_bootcmd"`;then
    $BIN/fw_setenv MBoot_bootcmd
    [ $? -gt 0 ] && GOTERROR "error removing MBoot_bootcmd"
fi
if `echo $myENV | egrep -q "bootargsusb|menu_|bootcmdusb|bootargshub|bootcmdhub|bootargside|bootcmdide"`; then
    for i in `cat /proc/partitions | grep sd[abcd]. | awk '{print $4}' | sed 's/sd.//'`
    do
        $BIN/fw_setenv "menu_$i"
        [ $? -gt 0 ] && GOTERROR "error removing menu_$i"
        $BIN/fw_setenv "bootargsusb$i"
        [ $? -gt 0 ] && GOTERROR "error removing  bootargsusb$i"
        $BIN/fw_setenv "bootcmdusb$i"
        [ $? -gt 0 ] && GOTERROR "error removing bootcmdusb$i"
        $BIN/fw_setenv "bootargshub$i"
        [ $? -gt 0 ] && GOTERROR "error removing bootargshub$i"
        $BIN/fw_setenv "bootcmdhub$i"
        [ $? -gt 0 ] && GOTERROR "error removing bootcmdhub$i"
        $BIN/fw_setenv "bootargside$i"
        [ $? -gt 0 ] && GOTERROR "error removing bootargside$i"
        $BIN/fw_setenv "bootcmdide$i"
        [ $? -gt 0 ] && GOTERROR "error removing bootcmdide$i"
    done
fi

if `cat /proc/mtd | grep -q 'mtd7:'`; then
	LOG "spark7162, we need to rmmod i2s.ko module after flashing"
	rmmod i2s.ko
fi

fi
touch /tmp/mboot.ok
sync
