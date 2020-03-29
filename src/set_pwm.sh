#!/bin/bash
set -uo pipefail
trap 's=$?; echo "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR
IFS=$'\n\t'

chip0=/sys/class/pwm/pwmchip0
pwm0=$chip0/pwm0
pwm1=$chip0/pwm1

echo $1*500000+1500000 | bc -l
echo 20000000.0  > $pwm0/duty_cycle
#echo "$u2" > $pwm1/duty_cycle
