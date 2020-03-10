#!/bin/bash
chip0=/sys/class/pwm/pwmchip0
pwm0=$chip0/pwm0
pwm1=$chip0/pwm1

pi_enable() {
    echo 0 > $chip0/export
    echo 1 > $chip0/export
    echo 20000000  > $pwm0/period
    echo 20000000  > $pwm1/period
    echo 1500000 > $pwm0/duty_cycle
    echo 1500000 > $pwm1/duty_cycle
    echo 1 > $pwm0/enable
    echo 1 > $pwm1/enable
}

pi_enable