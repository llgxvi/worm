#include <linux/syscalls.h>

uint64_t **get_table() {
  // sct: sys_call_table

  uint64_t offset = PAGE_OFFSET;
  uint64_t **sct;

  while(offset < ULLONG_MAX) {
    sct = (uint64_t**)offset;

    if(sct[__NR_close] == (uint64_t*)ksys_close) {
      printk("🍺 sys_call_table found at address: 0x%p\n", sct);
      return sct;
    }

    offset += sizeof(void*);
  }

  return NULL;
}

int f_init(void) {
  return 0;
}

void f_exit(void) {
}

MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
