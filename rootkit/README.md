### insert module
`insmod rooty.ko`

### remove module
`rmmod rooty`

### other
```
/proc/modules
/sys/module

dmesg -C
dmesg -T | grep rooty
dmesg -T | tail -n 1
lsmod | grep rooty
grep rooty /proc/modules
```

### replace 4 space to tab
`sed -i 's/ \{4\}/\t/g' Makefile`
