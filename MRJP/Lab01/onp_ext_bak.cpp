#include <cstdio>
#include <iostream>
#include <stack>
#include <cstdlib>
#include <cctype>

using namespace std;

#define MAX_L 1024
#define DEBUG true

struct Term
{
    int number;
    char op;
    bool isNumber;
}

class Tree
{
    char op;
    Tree right;
    Tree left;
    int wartosc()
    {
        
    }
    void toString()
    {
        printf("( ");
        left.toString();
        printf(" %c ", op);
        right.toString();
        printf(" )";
    }
};

class Leaf : Tree
{
    int number;
    int wartosc()
    {
        return number;
    }
};

int read_number_ext(int base, char* digits, int* i, char* inp)
{
    int number = 0;
    char* p;
    while(*i < MAX_L && (p = find(digits, digits + base, tolower(inp[*i]))) != digits + base)
	{
		number *= base;
		number += p - digits;
		(*i)++;
	}
    
	(*i)--;
    if(DEBUG) printf("read - %d\n", number);
    return number;
}

int read_number(int* i, char* inp)
{
    if(inp[*i] == '0' && (*i) + 1 < MAX_L && inp[(*i) + 1] == 'x')
    {
        (*i) = (*i) + 2;
        char digits[] = "0123456789abcdef";
        return read_number_ext(16, digits, i, inp);
    }
    char digits[] = "0123456789";
    return read_number_ext(10, digits, i, inp);
}

int main()
{
    char* inp = (char *)malloc(MAX_L);
    fgets(inp, MAX_L, stdin);
	for(int i = 0;i < MAX_L && inp[i] != 0 && inp[i] != '\n'; i++)
	{
		char c = inp[i];
		if(DEBUG) printf("read char - '%c'\n", c);
        if(isblank(c) != 0) continue;
        else if(isdigit(c)) st.push(read_number(&i, inp));
		else if(c == '-' && i < MAX_L && isdigit(inp[i + 1])) st.push(-read_number(&i, inp));
		else
		{
            if(c != '+' && c!='-' && c!='*' && c!='/' && c!='%')
            {
                printf("Unexpected character at position %d\n", i);
                perror("Unexpected char.");  return 1;
            }
            
            if(st.empty()) { perror("Number expected."); return 1; }
            int a = st.top();
            st.pop();
            if(st.empty()) { perror("Number expected."); return 1; }
            int b = st.top();
            st.pop();
			switch(c)
			{
				case '+': 
					st.push(a + b);
                    break;
                case '-':
					st.push(a - b);
                    break;
                case '*':
					st.push(a * b);
                    break;
                case '/':
                    if (b == 0) { perror("Divided by 0."); return 1; }
					st.push((int)(a / b));
                    break;
				case '%':
                    if (b == 0) { perror("Modulo by 0."); return 1; }
					st.push(a % b);
                    break;
			}
		}
	}
    
    int result = 0;
    if(!st.empty())
    {
        result = st.top();
        st.pop();
        if(!st.empty())
        {
            perror("Not enough numbers."); return 1;
        }
    }
    
    printf("Result of the expression is %d\n", result);

    free(inp);

    return 0;
}
