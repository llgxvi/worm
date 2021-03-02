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
  int word_l = strlen(word);
  int data_l = strlen(data);
  char word_tmp[DEVICE_SIZE - 1];

  int i = word_l - 1;
  int j = 0;
  for(; i >= 0; i--, j++)
    word_tmp[j] = word[i];

  word_tmp[word_l] = '\0';

  if(first) {
    first = 0;
    memset(data, '\0', sizeof(data));
    strcpy(data, word_tmp);
  }
  else {
    data[data_l] = ' ';
    data[data_l + 1] = '\0';
    strcat(data, word_tmp);
  }
}

void reverse(char *data_tmp) {
  int data_tmp_l = strlen(data_tmp);
  char word[DEVICE_SIZE - 1];

  int i = data_tmp_l - 1;
  int j = 0;
  for(; i >= 0; i--, j++) {
    if(data_tmp[i] != ' ') {
      word[j] = data_tmp[i];
      if(i == 0) {
        word[j + 1] = '\0';
        insert_word(word);
        data[data_tmp_l] = '\0';
        first = 1;
        printk("🥤 %s\n", word);
        printk("⚽️ %s\n", data);
      }
    }
    else {
      word[j] = '\0';
      insert_word(word);
      j = -1;
      printk("🍺 %s\n", word);
    }
  }
}

//
ssize_t f_read(struct file *f, char *buff, size_t len, loff_t *off) {
  if(copy_to_user(buff, data, strlen(data)) != 0) {
    printk("⚠️ copy_to_user\n");
    return -1;
  }

  return strlen(data);
}

ssize_t f_write(struct file *f, const char *buff, size_t len, loff_t *off) {
  // copy_from_user doesn't append \0
  char data_tmp[DEVICE_SIZE - 1] = {0};

  if(copy_from_user(data_tmp, buff, len) != 0) {
    printk("⚠️ copy_from_user\n");
    return -1;
  }

  printk("🥃 %s %ld\n", data_tmp, strlen(data_tmp));
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
