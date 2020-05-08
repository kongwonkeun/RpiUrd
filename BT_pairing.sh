#!/usr/bin/expect -f

set prompt "#"
set address [lindex $argv 0]

spawn bluetoothctl
expect -re $prompt
send "remove $address\r"
sleep 2
expect -re $prompt
send "scan on\r"
sleep 16
send "scan off\r"
expect "Controller"
send "trust $address\r"
sleep 2
send "pair $address\r"
sleep 2
send "1234\r"
sleep 3
send "quit\r"
expect eof

#