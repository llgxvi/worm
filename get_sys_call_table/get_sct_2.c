#include <linux/syscalls.h>

unsigned long *get_sct(void) {
  unsigned long *sct;
  unsigned long i;

  i = (unsigned long)ksys_close;
  for(; i < ULONG_MAX; i += sizeof(void*)) {
    sct = (unsigned long *)i;

    if(sct[__NR_close] == ksys_close) {
      printk("🍺 sys_call_table found at address: 0x%p\n", sct);
      return sct;
    }
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
