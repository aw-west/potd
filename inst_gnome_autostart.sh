#!/usr/bin/env bash
ATSTRT_DIR=$HOME/.config/autostart  
if [ ! -d "$ATSTRT_DIR" ]; then
  mkdir $ATSTRT_DIR
fi
cp natgeo.desktop $ATSTRT_DIR
