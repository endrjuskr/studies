#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 50


int readInt()
{
    int i;
    scanf("%d", &i);
    return i;
}

void printInt(int i)
{
    printf("%d\n", i);
}

char* readString()
{
    char* s = (char *)malloc(MAX_LENGTH+1);
    scanf("%s", s);
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
    strcpy(s, b);
    return s;
}

void error()
{
    char[] s = "runtime error\n";
    printf("%s", s);
    return 1;
}
