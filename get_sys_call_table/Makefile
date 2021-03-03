N=get_sys_call_table

obj-m += $N.o

all:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

test:
    insmod $N.ko
    rmmod $N
    dmesg -T | tail -n 5
