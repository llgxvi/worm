###
http://manpages.ubuntu.com/manpages/focal/man2/getdents64.2.html

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
```

https://stackoverflow.com/questions/31396090/kernel-sys-call-table-address-does-not-match-address-specified-in-system-map
