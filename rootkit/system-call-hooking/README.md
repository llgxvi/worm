https://security.stackexchange.com/questions/210897/why-is-there-a-need-to-modify-system-call-tables-in-linux

```
man getdents64

int getdents64(
  unsigned int fd, 
  struct linux_dirent64 *dirp,
  unsigned int count
)

struct linux_dirent64 {
  ino64_t        d_ino;
  off64_t        d_off;
  unsigned short d_reclen;
  unsigned char  d_type;
  char           d_name[];
};

struct linux_dirent {
  unsigned long  d_ino;
  unsigned long  d_off;
  unsigned short d_reclen;
  char           d_name[];
  char           pad;
  char           d_type;
};
```

### sys_call_table
```
grep sys_call_table /boot/System.map-$(uname -r)
grep sys_call_table /proc/kallsyms
```

https://stackoverflow.com/questions/28936630/what-is-the-need-of-having-both-system-map-file-and-proc-kallsyms
https://stackoverflow.com/questions/31396090/kernel-sys-call-table-address-does-not-match-address-specified-in-system-map

### One's Complement Operator
https://stackoverflow.com/questions/791328/how-does-the-bitwise-complement-operator-tilde-work
