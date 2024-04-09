#!/bin/bash
tmux new-session -d -s printer
tmux new-window -t printer:1 -n 'printer' 'cd ~/madpeset && python txt.py'
tmux attach-session -t printer
