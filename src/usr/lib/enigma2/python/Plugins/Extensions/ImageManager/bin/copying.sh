#!/bin/sh
#Created by Vasiliks 06.11.2015
#last edited 08.2016  
LABEL_FROM=$1 ; PART_FROM=$2
LABEL_TO=$3 ; PART_TO=$4
LANG='en'
if grep -qs 'config.osd.language=ru_RU' /etc/enigma2/settings ; then LANG='ru' ; fi   
MESSAGE(){ if [ $LANG = "ru" ]; then echo "$2"; else echo "$1"; fi }
umount -l "$PART_TO"  2>/dev/null
rm -rf /tmp/from
mkdir -p /tmp/from
rm -rf /tmp/copy
mkdir -p /tmp/copy

if  [[ "$LABEL_FROM" = "NAND" ]] ; then
  mount -t jffs2 /dev/mtdblock6 /tmp/from
else
  mount $PART_FROM /tmp/from
fi
MESSAGE "Partition $LABEL_FROM mounted\n" "Раздел $LABEL_FROM примонтирован\n"
/sbin/tune2fs -L $6 $4 2>&1 | tee >/dev/null
MESSAGE "Partition PART_TO renamed to $6\n" "Раздел PART_TO переименован в $6\n"
mount $PART_TO /tmp/copy
MESSAGE "Please wait, is cleaning partition $PART_TO\n" "Подождите, идет очистка раздела $PART_TO\n "
rm -rf /tmp/copy/*
MESSAGE "Partition $PART_TO mounted\n" "Раздел $PART_TO примонтирован\n"
MESSAGE "Please wait, there is a copying" "Пожалуйста подождите, идет копирование"
MESSAGE "of the partition $PART_FROM($LABEL_FROM) for $PART_TO partition\n" "с раздела $PART_FROM($LABEL_FROM) на раздел $PART_TO\n"
(cd /tmp/from && tar cf - .) | (cd /tmp/copy && tar xf -)
if [ ! -f /tmp/copy/boot/uImage ] ; then    
    MESSAGE "Creating uImage" "Создается uImage"
    pathTOfind="/usr/bin /usr/sbin /sbin /bin"
    rezult=`find $pathTOfind -type l -name 'hexdump'`      
  if [[ "$rezult" = '' ]]; then
      dd if=/dev/mtd5 of=/tmp/copy/boot/uImage bs=4096 count=768
  else
      set `dd if=/dev/mtd5 bs=4 skip=3 count=1 | hexdump -C | head -n1`
      Z=$((64 + `printf "%d" 0x$2$3$4$5`))
      dd if=/dev/mtd5 of=/tmp/copy/boot/uImage bs=$Z count=1
  fi   
fi
if [[ "$5" = "YES" ]]; then
  rm -rf /tmp/copy/etc/enigma2/settings
  MESSAGE "Enigma2 settings deleted\n" "Файл настроек Enigma2 settings удален\n"
fi
cd /
sync
sleep 2
umount /tmp/copy
MESSAGE "Partition $LABEL_FROM unmounted\n" "Раздел $LABEL_FROM отмонтирован\n"
umount /tmp/from
MESSAGE "Partition $PART_TO unmounted\n" "Раздел $PART_TO отмонтирован\n"
rm -rf /tmp/from
rm -rf /tmp/copy
exit
