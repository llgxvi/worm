CONFIG_MODULE_SIG=n
CONFIG_MODULE_SIG_ALL=n

N=simple_char_device

obj-m += $N.o

all:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

test:
    insmod $N.ko
    rmmod $N
    dmesg -T | tail -n 5
