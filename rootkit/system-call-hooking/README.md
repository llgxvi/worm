###
http://manpages.ubuntu.com/manpages/focal/man2/getdents64.2.html

```
man getdents64

int getdents64(
  unsigned int fd, 
  struct linux_dirent64 *dirp,
  unsigned int count
)

struct linux_dirent {
  unsigned long  d_ino;
  unsigned long  d_off;
  unsigned short d_reclen;
  char           d_name[];
  char           pad;
  char           d_type;
}

```
