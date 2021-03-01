#include <linux/module.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>

// TODO
#include <asm/uaccess.h>
#include <linux/uaccess.h>

#define NAME "simple_char_device"
#define DEVICE_SIZE 512

char data[DEVICE_SIZE+1]="no data has been written yet";

//
void insert_word(char *word, unsigned int n)
{
  int i, c;
  char tmpword[DEVICE_SIZE+1];

  for(i=strlen(word)-1, c=0; i >= 0; i--, c++)
    tmpword[c] = word[i];
  
  tmpword[strlen(word)] = '\0';

  if(n == 0) {
    memset(data, 0, sizeof data);
    strcpy(data, tmpword);
  } 
  else {
    data[strlen(data)] = ' ';
    data[strlen(data)+1] = '\0';
    strcat(data, tmpword);
  }
}

void reverse(char *data_tmp) {
  int i = strlen(data_tmp) - 1;
  int j = 0;
  int n = 0;
  char word[DEVICE_SIZE+1];

  for(; i >= 0; i--, j++) {
    if(data_tmp[i] != ' ')
      word[j] = data_tmp[i];
    else {
      word[j] = '\0';
      insert_word(word, n);
      n += 1;
      j = -1;
    }
  }

  word[j] = '\0';
  insert_word(word, n);
  data[i+1] = '\0';
}

//
ssize_t reverse_read(
        struct file *fp,
        char *buff,
        size_t len,
        loff_t *off) {
  ssize_t b = copy_to_user(buff, data, strlen(data));

  if(b != 0) {
    printk("Kernel -> userspace copy failed\n");
    return -1;
  }

  return strlen(data);
}

ssize_t reverse_write(
        struct file *fp,
        const char *buff,
        size_t len,
        loff_t *off) {
  char data_tmp[DEVICE_SIZE+1];

  ssize_t b = copy_from_user(data_tmp, buff, len)

  if(b != 0) {
    printk("Userspace -> kernel copy failed\n");
    return -1;
  }

  reverse(data_tmp);
  return 0;
}

// file ops
struct file_operations fops = {
  read: reverse_read,
  write: reverse_write
};

// misc device
struct miscdevice md = {
  .minor = MISC_DYNAMIC_MINOR,
  .name = NAME,
  .fops = &fops
};

//
int f_init(void) {
  misc_register(&md);
  printk("%s loaded\n", NAME);
  return 0;
}

void f_exit(void) {
  misc_deregister(&md);
  printk("%s removed\n", NAME);
}

//
MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
