Obj-m := rooty.o

KERNEL_DIR=/lib/modules/$(uname -r)/build

all:
  $(MAKE) -C $(KERNEL_DIR) M=$(PWD)
