#!/bin/sh
#Created by Vasiliks 06.11.2015
#last edited 11.2015
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
MESSAGE "Partition $4 renamed to $6\n" "Раздел $4 переименован в $6\n"
mount $PART_TO /tmp/copy
rm -rf /tmp/copy/*

MESSAGE "Partition $PART_TO mounted\n" "Раздел $PART_TO примонтирован\n"

if [[ "$5" = "YES" ]]; then
  mv /tmp/from/etc/enigma2/settings /tmp
  MESSAGE "Enigma2 settings deleted" "Файл настроек Enigma2 settings удален"
fi

MESSAGE "Please wait, there is a copying" "Пожалуйста подождите, идет копирование"
MESSAGE "of the partition $LABEL_FROM for $PART_TO partition\n" "с раздела $LABEL_FROM на раздел $PART_TO\n"

(cd /tmp/from && tar cf - .) | (cd /tmp/copy && tar xf -)

if [[ "$5" = "YES" ]]; then
  mv /tmp/settings /tmp/from/etc/enigma2
fi

cd /
sync
sleep 2
umount /tmp/copy
MESSAGE "Partition $LABEL_FROM unmounted\n" "Раздел $LABEL_FROM отмонтирован\n"
umount /tmp/from
MESSAGE "Partition $6 unmounted\n" "Раздел $6 отмонтирован\n"
rm -rf /tmp/from
rm -rf /tmp/copy
exit
