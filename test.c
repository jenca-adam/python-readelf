#include    <stdio.h>

#pragma init (foo)
#pragma fini (bar)

void foo()
{
        (void) printf("initializing: foo()\n");
}

void bar()
{
        (void) printf("finalizing: bar()\n");
}

void main()
{
        (void) printf("main()\n");
}

