#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
module_init(rooty_init);
module_exit(rooty_exit);

int rooty_init(void) {
  printk("rooty: module loaded\n");
  return 0;
}

void rooty_exit(void) {
  printk("rooty: module removed\n");
}
