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
  char mode;  // r, w
  char str[SIZE];
  int len;
  int fd;

  mode = argv[1][0];
  if(mode == 'w') {
    strcpy(str, argv[2]);
    len = strlen(str);
  }

  fd = open("/dev/"DEVICE, O_RDWR);
  if(fd == -1) {
    perror("⚠️ device");
    exit(1);
  }

  if(mode == 'w') {
    if(write(fd, str, len) == 0)
      printf("write to device ✅\n");
    else
      perror("⚠️ write");
  }

  if(mode == 'r') {
    if(read(fd, buf, strlen(buf)) != -1) {
      printf("read from device ✅\n");
      printf("%s\n", buf);
    }
    else
      perror("⚠️ read");
  }

  close(fd);
  exit(0);
}
