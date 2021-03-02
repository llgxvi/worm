#include <linux/module.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/fs.h>

// TODO
#include <asm/uaccess.h>
#include <linux/uaccess.h>

#define NAME "simple_char_device"
#define DEVICE_SIZE 512

char data[DEVICE_SIZE - 1] = "no data has been written yet";
int first = 1;

//
void insert_word(char *word) {
  int word_len = strlen(word);
  int data_len = strlen(data);
  char word_tmp[DEVICE_SIZE - 1];

  int i = word_len - 1;
  int j = 0;
  for(; i >= 0; i--, j++)
    word_tmp[j] = word[i];

  word_tmp[word_len] = '\0';

  if(first) {
    first = 0;
    memset(data, '\0', sizeof(data));
    strcpy(data, word_tmp);
  } 
  else {
    data[data_len] = ' ';
    data[data_len + 1] = '\0';
    strcat(data, word_tmp);
  }
}

void reverse(char *data_tmp) {
  int data_tmp_len = strlen(data_tmp);
  char word[DEVICE_SIZE - 1];

  int i = data_tmp_len - 1;
  int j = 0;
  for(; i >= 0; i--, j++) {
    if(data_tmp[i] != ' ') {
      word[j] = data_tmp[i];
      if(i == 0) {
        word[j + 1] = '\0';
        insert_word(word);
        data[data_tmp_len] = '\0';
        first = 1;
      }
    }
    else {
      word[j] = '\0';
      insert_word(word);
      j = -1;
    }
    printk("🍺 %s", word);
  }
}

//
ssize_t f_read(struct file *f, char *buff, size_t len, loff_t *off) {
  ssize_t b = copy_to_user(buff, data, strlen(data));

  if(b != 0) {
    printk("Kernel -> userspace copy failed\n");
    return -1;
  }

  return strlen(data);
}

ssize_t f_write(struct file *f, const char *buff, size_t len, loff_t *off) {
  char data_tmp[DEVICE_SIZE - 1];

  ssize_t b = copy_from_user(data_tmp, buff, len);

  if(b != 0) {
    printk("Userspace -> kernel copy failed\n");
    return -1;
  }

  reverse(data_tmp);
  return 0;
}

// file ops
struct file_operations fops = {
  read: f_read,
  write: f_write
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
  printk(KERN_INFO "%s loaded\n", NAME);
  return 0;
}

void f_exit(void) {
  misc_deregister(&md);
  printk(KERN_INFO "%s removed\n", NAME);
}

//
MODULE_LICENSE("GPL");
module_init(f_init);
module_exit(f_exit);
