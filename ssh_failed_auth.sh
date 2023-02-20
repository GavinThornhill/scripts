#!/bin/bash
AUTH_LOG=/var/log/auth.log
FOLDER=/tmp/failed_ssh
TEMP_LOG=$FOLDER/tmp_secure.log
NUMBER=$FOLDER/number.txt

echo "HOSTNAME: `hostname`"

check_folder () {
	if [[ -d $FOLDER ]]; then
	if [[ ! -s $NUMBER ]]; then
		touch $NUMBER
		echo 0 > $NUMBER
	fi
	else
		mkdir -p $FOLDER
		touch $NUMBER
		echo 0 > $NUMBER
	fi
}

get_log () {
	NUM=`cat $NUMBER`
	SUM=`expr "$NUM" + 1`
	tail -n +"$SUM" $AUTH_LOG > $TEMP_LOG
	echo `wc -l < $AUTH_LOG` > $NUMBER
}

failed_ssh () {
	egrep "Failed password" $AUTH_LOG | awk '{print $9 ": " $11}' | cut -d ';' -f1 | sed '/^\s*$/d' | uniq -c | sort -nr | awk 'int($1)>=5'
}

check_folder
get_log
failed_ssh