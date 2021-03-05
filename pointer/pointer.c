#include <stdio.h>

// p2 -> p1 -> n
int main(void) {
  int n=123;
  int *p1;
  int **p2;

  p1 = &n;
  p2 = &p1;

  // value of n
  // n == *p1 == **p2
  printf("value of n:\n");
  printf("%d\n", n);
  printf("%d\n", *p1);
  printf("%d\n", **p2);
  printf("\n");

  // addr of n
  // &n == p1 == *p2
  printf("addr of n:\n");
  printf("%p\n", &n);
  printf("%p\n", p1);
  printf("%p\n", *p2);
  printf("\n");

  // value of p1
  // p1 == *p2
  printf("value of p1:\n");
  printf("%p\n", p1);
  printf("%p\n", *p2);
  printf("\n");

  // addr of p1
  // &p1 == p2
  printf("addr of p1:\n");
  printf("%p\n", &p1);
  printf("%p\n", p2);

  return 0;
}
