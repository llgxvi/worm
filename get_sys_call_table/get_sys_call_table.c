#include <linux/syscalls.h>

// sct: sys_call_table
uintptr_t *get_sct(void) {
  // ksys_close:  kernel version > 5.3
  // PAGE_OFFSET: kernel memory starting point
  // ULLONG_MAX:  unsigned long long int max value

  uintptr_t *sct;
  uintptr_t offset = PAGE_OFFSET;

  while(offset < ULLONG_MAX) {
    sct = (uintptr_t*)offset;

    if(sct[__NR_close] == (uintptr_t)ksys_close) {
      printk("🍺 sys_call_table found at address: 0x%p\n", sct);
      return sct;
    }

    offset += sizeof(void*);
  }

  return NULL;
}

int f_init(void) {
  if(get_sct() == NULL)
    return -1;

  return 0;
}

void f_exit(void) {
}

MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
