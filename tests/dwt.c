#include<stdio.h>

extern void print_helloworld(int repeats){
	for(int i=0; i<repeats; i++){
		printf("%d: Hello, World!\n", i);
	}
}
extern void segfault(){
	int *a = NULL;
	printf("%d\n", *a);
}
