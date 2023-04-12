#!/bin/bash

# Usage: measure-process.sh NAME_PROCESS OUT_FILE

# Prerequisites:
# sudo apt install htop html2text

echo q | htop -C | aha --line-fix | html2text -width 999 | grep -v "F1Help" | grep -v "xml version=" > $2

