#!/bin/bash

# Create a new window named 'printer' and set the layout and locale within that window
tmux new-window -n 'printer' 'cd ~/printme && python txt.py; bash'

# Capture the new window ID
new_window_id=$(tmux list-windows -F "#{window_id}" | tail -n 1)

# Loop through all sessions and set the new window as the current window
tmux list-sessions -F "#{session_id}" | while read -r session_id; do
    tmux select-window -t $session_id:$new_window_id
done
