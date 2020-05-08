#!/usr/bin/expect -f

set prompt "#"
set address [lindex $argv 0]

spawn bluetoothctl
expect -re $prompt
send "agent off\r"
sleep 2
send "power off\r"
sleep 2
send "quit\r"
expect eof

#