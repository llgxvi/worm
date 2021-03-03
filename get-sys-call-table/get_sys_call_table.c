#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/unistd.h>

uint64_t **get_table(void) {
  uint64_t offset = PAGE_OFFSET;
  uint64_t **sct;

  while(offset < ULLONG_MAX) {
    sct = (uint64_t **)offset;

    if(sct[__NR_close] == (uint64_t *) sys_close) {
      printk("🍺 sys_call_table found at address: 0x%p\n", sys_call_table);
      return sct;
    }

    offset += sizeof(void *);
  }

  return NULL;
}

int f_init(void) {
  int a = get_table();
  printk("🍺 %lu\n", (void*)a);
  return 0;
}

void f_exit(void) {
}

MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
