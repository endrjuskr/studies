#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LENGTH 1024


int readInt()
{
    int i;
    scanf("%d\n", &i);
    return i;
}

void printInt(int i)
{
    printf("%d\n", i);
}

char* readString()
{
    char *s;
    char c;
    s = (char *)malloc(MAX_LENGTH+1);
    int i = 0;
    while((c = getchar()) != '\n')
    {
        s[i++] = c;
    }

    return s;
}

void printString(char* s)
{
    printf("%s\n", s);
}

char* contactString(char* a, char* b)
{
    char* s = (char *)malloc(strlen(a) + strlen(b) + 1);
    strcpy(s, a);
    strcat(s, b);
    return s;
}

void error()
{
    char* s = "runtime error\n";
    printf("%s", s);
    exit(1);
}

void* initArray(int length, int size)
{
    printf("alloc\n");
    void * a = calloc(length, size);
    return a;
}
