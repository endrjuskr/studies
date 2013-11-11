#include <cstdio>
#include <iostream>
#include <stack>
#include <cstdlib>

using namespace std;

#define MAX_L 1024
#define DEBUG true
stack<int> st = stack<int>();

int read_number(int* i, char* inp)
{
	int number = 0 ;
	while(*i < MAX_L && isdigit(inp[*i]))
	{
		number *= 10;
		number += (int)inp[*i] - (int)'0';
		(*i)++;
	}
	(*i)--;
    if(DEBUG) printf("read - %d\n", number);
	return number;
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
                perror("Unexpected char."); return 1;
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
