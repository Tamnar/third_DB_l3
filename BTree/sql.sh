#!/bin/bash
#IFS=$'\n'
clear

pygmentize -g -O style=emacs ./BTree.sql

# for filePath in $(find -name '*.h' -print0 | xargs --null -n 1 echo| cut -c 3-); do
# 	echo "-----------Файл: \"$filePath\"-----------"
# 	pygmentize -g -O style=pastie $filePath
# 	printf "\n"
# done
# for filePath in $(find -name '*.c' -print0 | xargs --null -n 1 echo| cut -c 3-); do
# 	echo "-----------Файл: \"$filePath\"-----------"
# 	pygmentize -g -O style=pastie $filePath
# 	printf "\n"
# done
