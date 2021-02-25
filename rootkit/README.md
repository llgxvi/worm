```
insmod rooty.ko
dmesg | grep rooty

rmmod rooty.ko
dmesg | grep rooty

# /proc/modules
# /sys/module

grep rooty /proc/modules
ls /sys/modules | grep rooty
modinfo rooty
modprobe -c | grep rooty
grep rooty /proc/kallsyms 


```
