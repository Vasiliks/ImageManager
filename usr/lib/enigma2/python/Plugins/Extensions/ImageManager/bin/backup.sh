#!/bin/sh
#Created by Vasiliks 22.03.2015
#last edited 23.12.2018
#version 2.6 added backup bz2
LABEL_FROM=$1   ; DEVS_FROM=$2
LABEL_TO=$3     ; DEVS_TO=$4
TYPE_ARCHIVE=$5 ; CLEAR_ARCHIVE=$6 ; CLEAR_EMU=$7
DATE=`date +%Y%m%d_%H%M`
BACKUPIMAGE="e2jffs2.img"
BACKUPTAR="$1.tar"
BACKUPTARGZ="$1.tar.gz"
BACKUPTARBZIP="$1.tar.bz2"

if grep -qs 'config.osd.language=ru_RU' /etc/enigma2/settings ; then
    LANG='ru' ;
elif grep -qs 'config.osd.language=uk_UA' /etc/enigma2/settings ; then
    LANG='uk'
else
    LANG='en'
fi
MESSAGE(){ if [ $LANG = "ru" ]; then
             echo "$2"
           elif [ $LANG = "ru" ]; then
             echo "$3"
           else
             echo "$1"
           fi }

  rm -rf /tmp/root
  mkdir -p /tmp/root

  rm -rf /tmp/copy
  mkdir -p /tmp/copy

  if  [[ "$LABEL_FROM" = "NAND" ]] ; then
	mount -t jffs2 /dev/mtdblock6 /tmp/root
    MESSAGE "Creating uImage" "Создается uImage" "Створюється uImage"
    pathTOfind="/usr/bin /usr/sbin /sbin /bin"
    rezult=`find $pathTOfind -type l -name 'hexdump'`
    if [[ "$rezult" = '' ]]; then
      dd if=/dev/mtd5 of=/tmp/root/boot/uImage bs=4096 count=768
    else
      set `dd if=/dev/mtd5 bs=4 skip=3 count=1 | hexdump -C | head -n1`
      Z=$((64 + `printf "%d" 0x$2$3$4$5`))
      dd if=/dev/mtd5 of=/tmp/root/boot/uImage bs=$Z count=1
    fi
  else
    mount $DEVS_FROM /tmp/root
  fi
    MESSAGE "Partition $LABEL_FROM mounted\n" "Раздел $LABEL_FROM примонтирован\n" "Розділ $LABEL_FROM примонтований\n"
#backup and clear settings enigma
  if [[ $CLEAR_ARCHIVE = "YES" ]]; then
    mv /tmp/root/etc/enigma2/settings /tmp
    MESSAGE "Enigma2 settings deleted" "Файл настроек Enigma2 settings удален" "Файл налаштувань Enigma2 settings видалений"
  fi
#backup and clear EMUsettings
  pathTOfind="/tmp/root/usr /tmp/root/var /tmp/root/etc/tuxbox"
  wicardd=mgcamd=oscam=''
  #backup and clear settings wicardd
  if [[ `echo $CLEAR_EMU | grep W` ]]; then
    wicardd=`find $pathTOfind -name 'wicardd.conf'`
    if [[ "$wicardd" != '' ]]; then
    cp $wicardd /tmp/wicarddtmp.conf
    MESSAGE "Wicardd settings deleted" "Настройки Wicardd удалены" "Налаштування Wicardd видалені"
    sed "s~.*account.*~account =~" -i $wicardd
    fi
  fi
  #backup and clear settings mgcamd
  if [[ `echo $CLEAR_EMU | grep M` ]]; then
    mgcamd=`find $pathTOfind -name 'newcamd.list'`
    if [[ "$mgcamd" != '' ]]; then
    cp $mgcamd /tmp/newcamdtmp.list
    MESSAGE "MgCamd settings deleted" "Настройки MgCamd удалены" "Налаштування MgCamd видалені"
    sed "s~.*CWS = .*$~CWS = server port login parol 01 02 03 04 05 06 07 08 09 10 11 12 13 14~g" -i $mgcamd
    fi
  fi
  #backup and clear settings oscam-ymod
  if [[ `echo $CLEAR_EMU | grep O` ]]; then
   oscam=`find $pathTOfind -name 'oscam.conf'`
   if [[ "$oscam" != '' ]]; then
   cp $oscam /tmp/oscamtmp.conf
   MESSAGE "Oscam settings deleted"  "Настройки Oscam удалены" "Налаштування MgCamd видалені"
   sed "s~.*newcamd.*$~[name newcamd server port login parol]~g" -i $oscam
   sed "s~.*cccam.*$~[name cccam server port login parol]~g" -i $oscam
   sed "s~.*cs357x.*$~[name cs357x server port login parol]~g" -i $oscam
   sed "s~.*cs378x.*$~[name cs378x server port login parol]~g" -i $oscam
   fi
  fi

  mount "$DEVS_TO" /tmp/copy
  mkdir -p /tmp/copy/enigma2-$DATE-$LABEL_FROM

  if [[ "$TYPE_ARCHIVE" = "IMG" ]]; then
    BACKUP=$BACKUPIMAGE
    MESSAGE "\nCopying uImage\n" "\nКопируется uImage\n" "\nКопіюється uImage\n"
    cp /tmp/root/boot/uImage /tmp/copy/enigma2-$DATE-$LABEL_FROM
    MESSAGE "Please wait, $BACKUP is created\n" "Пожалуйста подождите, создается $BACKUP\n" "Будь ласка зачекайте, створюється $BACKUP\n"
  mkfs.jffs2 --root=/tmp/root --faketime --output=/tmp/copy/enigma2-$DATE-$LABEL_FROM/$BACKUP -e 0x20000 -n

  elif [[ "$TYPE_ARCHIVE" = "TAR" ]]; then
    BACKUP=$BACKUPTAR
    MESSAGE "Please wait, $BACKUPTAR is created\n" "Пожалуйста подождите, создается $BACKUPTAR\n" "Будь ласка зачекайте, створюється $BACKUPTAR\n"
    cd /tmp/root
    tar -cf /tmp/copy/enigma2-$DATE-$LABEL_FROM/$BACKUP * 2>/dev/null

  elif [[ "$TYPE_ARCHIVE" = "TARGZ" ]]; then
    BACKUP=$BACKUPTARGZ
    cd /tmp/root
     MESSAGE "Please wait, $BACKUPTARGZ is created\n" "Пожалуйста подождите, создается $BACKUPTARGZ\n" "Будь ласка зачекайте, створюється $BACKUPTARGZ\n"
    tar -czf /tmp/copy/enigma2-$DATE-$LABEL_FROM/$BACKUP * 2>/dev/null

  elif [[ "$TYPE_ARCHIVE" = "TARBZIP" ]]; then
    BACKUP=$BACKUPTARBZIP
    cd /tmp/root
     MESSAGE "Please wait, $BACKUPTARBZIP is created\n" "Пожалуйста подождите, создается $BACKUPTARBZIP\n" "Будь ласка зачекайте, створюється $BACKUPTARBZIP\n"
    tar -cjf /tmp/copy/enigma2-$DATE-$LABEL_FROM/$BACKUP * 2>/dev/null
  fi

    #restore settings
    [ -f /tmp/settings ] && mv /tmp/settings /tmp/root/etc/enigma2
    #restore wicardd
    [ -f /tmp/wicarddtmp.conf ] && mv /tmp/wicarddtmp.conf $wicardd
    #restore mgcamd
    [ -f /tmp/newcamdtmp.list ] && mv /tmp/newcamdtmp.list $mgcamd
    #restore oscam
    [ -f /tmp/oscamtmp.conf ] && mv /tmp/oscamtmp.conf $oscam

  if [ -f /tmp/copy/enigma2-$DATE-$LABEL_FROM/$BACKUP ] ; then
    MESSAGE "Your $BACKUP can be found in:\n$LABEL_TO/enigma2-$DATE-$LABEL_FROM\n" "Ваш $BACKUP находится на:\n$LABEL_TO/enigma2-$DATE-$LABEL_FROM\n" "Ваш $BACKUP знаходиться на:\n$LABEL_TO/enigma2-$DATE-$LABEL_FROM\n"
  else
    MESSAGE "Sorry, Error  \n  Backup not created!\n" "Извините, произошла ошибка \n  Бекап не создан!\n" "Вибачте, виникла помилка \n  Бекап не створений!\n"
  fi
  cd /
    sync
    umount /tmp/copy
    umount /tmp/root
    MESSAGE "Partition $LABEL_FROM unmounted\n" "Раздел $LABEL_FROM отмонтирован\n" "Розділ $LABEL_FROM відмонтовано\n"
    rm -rf /tmp/copy
    rm -rf /tmp/root
exit
