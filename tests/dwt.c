#include<stdio.h>
#define TEST_MACRO_hi_hello 123456
typedef struct TEST {
    int a[128];
    int b[TEST_MACRO_hi_hello];
    int m[256][256];
    char *ziz;
} TEST;
extern void print_helloworld(int repeats, TEST a){
	for(int i=0; i<repeats; i++){
		printf("%d: Hello, World! %s\n", i, a.ziz);
	}
}
extern void segfault(){
	int *a = NULL;
	printf("%d\n", *a);
}
int main(){
    segfault();
}
