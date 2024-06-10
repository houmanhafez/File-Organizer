#!/bin/bash

source venv/bin/activate

python script.py &

PYTHON_PID=$!

read -p "Enter your browser (chrome, edge, firefox, brave, vivaldi, tor, chromium, arc): " browser

case $browser in
chrome)
    open -a "Google Chrome"
    ;;
edge)
    open -a "Microsoft Edge"
    ;;
firefox)
    open -a "Firefox"
    ;;
brave)
    open -a "Brave Browser"
    ;;
vivaldi)
    open -a "Vivaldi"
    ;;
tor)
    open -a "Tor Browser"
    ;;
chromium)
    open -a "Chromium"
    ;;
arc)
    open -a "Arc"
    ;;
*)
    echo "Browser not recognized. Please enter one of the specified browsers."
    ;;
esac

wait $PYTHON_PID
