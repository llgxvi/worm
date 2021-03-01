### insert module
`insmod rooty.ko`

### remove module
`rmmod rooty`

### other
```
/proc/modules
/sys/module

dmesg -T | grep rooty
dmesg -T | tail -n 1
lsmod | grep rooty
grep rooty /proc/modules
```
