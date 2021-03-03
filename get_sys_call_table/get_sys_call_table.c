#include <linux/syscalls.h>

uint64_t **get_table(void) {
  // sct: sys_call_table
  // ksys_close: kernel version > 5.3
  // PAGE_OFFSET: kernel memory starting point
  // ULLONG_MAX: unsigned long long int max value

  uint64_t **sct;
  uint64_t offset = PAGE_OFFSET;

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
  get_table();
  return 0;
}

void f_exit(void) {
}

MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
