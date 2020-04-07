#!/bin/sh

if [ -z "$CRYSTAL_PATH" ]; then
    CRYSTAL_PATH=/usr/share/crystal/src:lib
fi

if [ -z "$CRYSTAL_LIBRARY_PATH" ]; then
    CRYSTAL_LIBRARY_PATH=/usr/lib:/usr/local/lib
fi

CRYSTAL_PATH=$CRYSTAL_PATH \
CRYSTAL_LIBRARY_PATH=$CRYSTAL_LIBRARY_PATH \
    exec /usr/lib/crystal/bin/crystal "$@"
