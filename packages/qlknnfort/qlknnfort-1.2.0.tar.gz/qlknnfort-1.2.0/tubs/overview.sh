#!/bin/sh
#
# overview.sh : prettyprint list of active makefiles
#
# Invoked by "make overview" to pretty print the list of active makefiles.
# Tries to output something similar to "tree", but has a few limitations.
#
# Warning: pretty bad code follows.

indent=""
current="."

if [ x"$1" != x"1" ]; then
	fmtEND="\e[0m"
	fmtFIL="\e[31m"
	fmtDEF="\e[34m"
else
	fmtEND=""
	fmtFIL=""
	fmtDEF=""
fi

inside() {
	echo "$1" | grep -o "^$2" >/dev/null
}
defsfile() {
	echo "$1" | grep -o 'defs/.*\.make' >/dev/null
}

common() {
	# See https://stackoverflow.com/a/6973268
	printf "%s\n%s\n" "$1" "$2" | sed -e 'N;s/^\(.*\).*\n\1.*$/\1/'
}

output() {
	echo "O"
	echo "$name"
}

ascend() {
	echo "A"
	echo "$1"
	current="$1"
}
descend() {
	pat="$1";
	if [ -z "$pat" ]; then
		pat="///////////////"; # hack: avoid empty sed expression
	fi
	
	for step in $(echo "$current" | sed "s:$pat::" | sed 's:/: :'); do
		echo "D"
	done
	current="$1"
}

balance() {
	level=0
	
	while read line; do
		echo "$line"
		if [ x"$line" == x"A" ]; then
			level=$((level+1))
		elif [ x"$line" == x"D" ]; then
			level=$((level-1))
		fi
	done

	while [ x"$level" != x"0" ]; do
		echo "D"
		level=$((level-1))
	done
}

prettyprint() {
	indent=""

	last=""
	lastindent=""

	echo "."

	read next
	while [ ! -z "$next" ]; do
		line="$next"
		read next

		if [ x"$line" == x"O" ]; then
			item="$next"
			read next

			if [ x"$next" == x"D" ]; then
				last="$item"
				lastindent="$indent│"
			else
				echo -e "$indent├── ${fmtFIL}$item${fmtEND}"
			fi
		elif [ x"$line" == x"A" ]; then
			if [ ! -z "$last" ]; then
				echo -n "$lastindent" | sed 's/ $//';
				echo -e "└── ${fmtFIL}$last${fmtEND}";
				last=""
				lastindent=""
			fi

			item="$next"
			read next

			echo "$indent├── $item"
			indent="$indent│   ";
		elif [ x"$line" == x"D" ]; then
			indent="$(echo "$indent" | sed 's/│   $//')";
			lastindent="$(echo "$lastindent" | sed 's/│\(\s*\)$/ \1/')";
		fi
	done

	if [ ! -z "$last" ]; then
		echo -n "$lastindent" | sed 's/ $//';
		echo -e "└── ${fmtFIL}$last${fmtEND}";
	fi
}

for file in $(cat -); do
	dir="$(dirname $file)"
	name="$(basename $file)"

	if defsfile "$file"; then
		continue;
	fi

	if [ x"$dir" == x"$current" ]; then
		output "$name"
	elif inside "$dir" "$current"; then
		ascend "$dir"
		output "$name"
	else
		descend $(common "$dir" "$current")
		ascend "$dir"
		output "$name"
	fi
done | balance | prettyprint

echo -e "└── ${fmtDEF}defs/*.make (support files)${fmtEND}"

#EOF
