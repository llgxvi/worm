#include <stdio.h>
#include <paths.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>

#define DEVICE "simple_char_device"
#define SIZE 511

int main(int argc, char *argv[]) {
  char buf[SIZE];
  char mode[1];  // r, w
  char str[SIZE];
  int len;
  int fd;

  mode = argv[1];
  if(mode == 'w') {
    str = argv[2];
    len = strlen(str);
  }

  fd = open("/dev/"DEVICE, O_RDWR);
  if(fd == -1) {
    perror("⚠️ device");
    exit(1);
  }

  if(mode == 'w') {
    if(write(fd, str, len) == 0)
      printf("write to device ✅");
    else
      perror("⚠️ write");
  }

  if(mode == 'r') {
    if(read(fd, buf) != -1)
      printf("read from device ✅");
      printf("\n%s\n", str);
    else
      perror("⚠️ read");
  }

  close(fd);
  exit(0);
}
