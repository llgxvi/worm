### 🍺
input (device is written to): string
output (device is read from): string

This character device will:
take a string when written to,
reverse the string,
output the reversed string when read from.

### original
https://exploit.ph/linux-kernel-hacking/2014/06/06/a-simple-character-device/

### copy to user
https://www.kernel.org/doc/htmldocs/kernel-api/API---copy-to-user.html
https://stackoverflow.com/questions/59000547/clear-buffer-user-data-before-doing-another-write-on-a-linux-device-driver

Clear buffer in user space
before `copy_to_user()` again,
it doesn't append `\0`,
if the last copy is longer,
extra characters will appear at the end.
Solution `memset(buf, '\0', sizeof(buf))`

### copy from user
https://www.kernel.org/doc/htmldocs/kernel-api/API---copy-from-user.html

`copy_from_user()` doesn't append `\0`

### other
`printk()` must have `\n` for guaranteed showing with `dmesg`

simple_char_device: module verification failed: signature and/or required key missing - tainting kernel
