#!/bin/bash

icondir="$1"

max_icons=100000

if [[ -z "$icondir" ]]; then
	echo "Usage: purge_icons.sh /path/to/icon/cache"
	exit 1
fi

function count_icons() {
	$(find "$icondir" -type f | wc -l)
}

function purge_old_icons() {
	local age="$1"
	$(find "$icondir" -type f -atime +${age} -exec rm -f {} \;)
}

icon_count=$(count_icons)
delta=7
while [ $icon_count -gt $max_icons ]
do
	purge_old_icons $delta
	icon_count=$(count_icons)
	delta=$(( $delta - 1 ))
done

if [[ $icon_count -lt $max_icons ]]; then
	echo "$icon_count icons cached"
	exit 0
fi

old_icons=$(find . -type f -atime +5 | wc -l)
echo "$old_icons old icons to delete"

