CONFIG_MODULE_SIG=n
CONFIG_MODULE_SIG_ALL=n

obj-m += simple_char_device.o

all:
make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

test:
dmesg -C
insmod simple_char_device.ko
rmmod simple_char_device
dmesg -T
