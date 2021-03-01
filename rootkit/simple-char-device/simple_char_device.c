#include <linux/module.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>

#TODO
#include <asm/uaccess.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");

#define NAME "simple_char_device"
#define DEVICE_SIZE 512

char data[DEVICE_SIZE+1]="no data has been written yet";

//
void insert_word(char *word, unsigned int n)
{
  int i, c;
  char tmpword[DEVICE_SIZE+1];

  for (i=strlen(word)-1, c=0; i >= 0; i--, c++)
    tmpword[c] = word[i];
  
  tmpword[strlen(word)] = '\0';

  if (n == 0) {
    memset(data, 0, sizeof data);
    strcpy(data, tmpword);
  } 
  else {
    data[strlen(data)] = ' ';
    data[strlen(data)+1] = '\0';
    strcat(data, tmpword);
  }
}

void reverse(char *tmpdata) {
  int l;
  int i, c;
  unsigned int n = 0;
  char word[DEVICE_SIZE+1];

  l = strlen(tmpdata)-1;

  for(i=l, c = 0; i >= 0; i--, c++) {
    if (tmpdata[i] == ' ') {
      word[c] = '\0';
      insert_word(word, n);
      n += 1;
      c = -1;
    } 
    else
      word[c] = tmpdata[i];
  }

  word[c] = '\0';
  insert_word(word, n);
  data[strlen(tmpdata)] = '\0';
}

//
ssize_t reverse_read(
        struct file *filep,
        char *buff,
        size_t count,
        loff_t *offp) {
  if(copy_to_user(buff,data,strlen(data)) != 0) {
    printk( "Kernel -> userspace copy failed!\n");
    return -1;
  }

  return strlen(data);
}

ssize_t reverse_write(
        struct file *filep,
        const char *buff,
        size_t count,
        loff_t *offp) {
  char tmpdata[DEVICE_SIZE+1];

  if (copy_from_user(tmpdata,buff,count) != 0) {
    printk( "Userspace -> kernel copy failed!\n");
    return -1;
  }

  reverse(tmpdata);
  return 0;
}

// file ops
struct file_operations fops = {
  read: reverse_read,
  write: reverse_write
};

// misc device
static struct miscdevice md = {
  .minor = MISC_DYNAMIC_MINOR,
  .name = NAME,
  .fops = &fops
};

//
int reverse_init(void) {
  misc_register(&md);
  printk("%s loaded\n", NAME);
  return 0;
}

void reverse_exit(void) {
  misc_deregister(&md);
  printk("%s removed\n", NAME);
}

//
module_init(reverse_init);
module_exit(reverse_exit);
