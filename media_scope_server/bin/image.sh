#!/bin/sh

a=0
for file in *.py
do 
	echo "Counting file $file ..."
#	convert -resize 816x612 $file $file
	wc -l $file
#	mv $file $a.jpg
#	adb push $a.jpg /sdcard/DCIM/Camera/
	a=$(($a + 1))
done
