#!/usr/bin/expect -f

set prompt "#"
set address [lindex $argv 0]

spawn bluetoothctl
expect -re $prompt
send "power on\r"
sleep 2
send "agent on\r"
sleep 2
send "quit\r"
expect eof

#