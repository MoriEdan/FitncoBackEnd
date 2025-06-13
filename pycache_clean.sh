#!/bin/sh

if [ "$1" ]; then
  WHERE="$1"
else
  WHERE="$PWD"
fi

find "$WHERE" \
  -name '__pycache__' -delete -print \
  -o \
  -name '*.pyc' -delete -print
