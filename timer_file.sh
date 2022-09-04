# Parameters inserts sleep time in minutes
sleep $((60*$1)) && \
osascript -e 'display notification "Take a break from the screen for 20 Seconds or longer."'
