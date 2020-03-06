#!/bin/bash
chip0=/sys/class/pwm/pwmchip0
pwm0=$chip0/pwm0
pwm1=$chip0/pwm1

pwm0() {
    echo $1*500000+1500000 > $pwm0/duty_cycle
}

pwm1() {
    echo $1*500000+1500000 > $pwm1/duty_cycle
}

pwm0 $1
pwm1 $2