#!/bin/bash

dir="$(dirname "$(realpath "$0")")";
makefile="$(realpath "${dir}/../Makefile")";

if ! grep -e 'include .*tubs/main.make' "${makefile}" >/dev/null 2>&1; then
    echo "No TUBS-importing Makefile found, abort!" >&2;
    exit 1
fi

echo "${makefile}"
IFS='\n' readarray -t  files < <(find "$(dirname "$makefile")" \( -name '*.o' -or -name '*.a' -or -name '*.mod' -or -name '*.exe' \) -print)
if [[ "${#files[@]}" -eq 0 ]]; then
    echo "No purgable files found, nothing to do"
    exit 0
fi

echo "Found purgable files:"
echo "${files[@]}";

read -p "Purge files [Y/n] " yno
if [ -z "$yno" ]; then
  echo Y
  yno=Y
fi

case "$yno" in
  Y | y)
    echo "Purging files"
    rm "${files[@]}"
    ;;
  N | n)
    echo "Not purging files"
    exit 0
    ;;
esac
