#!/bin/bash

function move_win {
    if [ -z "$1" ]; then
        echo -e "Specify a screen, possible options: "
        echo -e $(xrandr | grep " connected " | cut -d'-' -f1)
        return
    fi

    MONITOR=$1

    # get all relevant windows on all screens
    windows=$(wmctrl -l | egrep -v " -1 " | cut -d" " -f1)

    if [ ! -z "$windows" ]; then
        # get the necessary metrics from the screen the windows should be moved to 
        # will contain: width, height, offsetX, offsetY
        screen_values=($(xrandr | grep "^$MONITOR-.* connected" | grep -Eo '[0-9]+x[0-9]+\+[0-9]+\+[0-9]+' | sed 's/x/ /g; s/+/ /g'))

        if (( ${#screen_values[@]} )); then
            # get the start/end position of the screen so we can later determine
            # if the window is already on the screen or not
            screen_start_pos=$(( ${screen_values[2]} ))
            screen_end_pos=$(( ${screen_values[2]} + ${screen_values[0]} ))

            for window in $windows; do
                # get the window name
                window_name=$(wmctrl -lG | grep "$window" | awk -F "$HOSTNAME " '{print $2}')
                # extract relevant window geometry values such as x, y, width, height
                window_values=($(wmctrl -lG | grep "$window" | awk -F " " '{print $3, $5, $6}'))

                # if the window's X origin position is already inside the screen's 
                # total width then don't move it (this won't work exactly for windows only partially on the screen)
                if (( ${window_values[0]} >= $screen_end_pos || ${window_values[0]} < $screen_start_pos )); then
                    echo -e "Moving to screen $MONITOR: $window_name"
                  
                    wmctrl -ir $window -b remove,maximized_vert
                    wmctrl -ir $window -b remove,maximized_horz
                    # the -e parameters are gradient,x,y,width,height
                    # move window to (X,Y) -> (0,0) of new screen and the same window dimensions
                    wmctrl -ir $window -e 0,$screen_start_pos,0,${window_values[1]},${window_values[2]}
                else
                    echo -e "Already on screen $MONITOR: $window_name"
                fi
            done
        else 
            echo -e "No screen found"
        fi
    else
        echo -e "No windows found"
    fi
}

move_win $1