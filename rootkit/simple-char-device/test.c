#include <stdio.h>
#include <paths.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

#define DEVICE "simple_char_device"
#define SIZE 511

static char buf[SIZE];

int main(int argc, char *argv[]) {
  int fd = open("/dev/" DEVICE, O_RDWR);
  int len = strlen(argv[1]);

  if(len > SIZE) {
    printf("⚠️ String too long\n");
    exit(0);
  }

  if(fd == -1) {
    perror("/dev/" DEVICE);
    exit(1);
  }

  printf("fd: %d\n", fd);

  if(read(fd, buf, len) == -1)
    perror("read()");
  else
    printf("Before: %s\n", buf);

  if(write(fd, argv[1], len) == -1)
    perror("write()");
  else
    printf("Wrote: %s\n", argv[1]);

  buf = memset(buf, 0, strlen(buf) * sizeof(buf));

  if(read(fd, buf, len) == -1)
    perror("read()");
  else
    printf("After: %s\n", buf);

  if((close(fd)) == -1) {
    perror("close()");
    exit(1);
  }

  exit(0);
}
