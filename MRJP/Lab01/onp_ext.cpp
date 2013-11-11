#include <cstdio>
#include <iostream>
#include <stack>
#include <string>
#include <cstdlib>
#include <cctype>

using namespace std;

#define MAX_L 1024
#define DEBUG true

struct term
{
    int number;
    char op;
    bool isNumber;
};

class Tree
{
    char op;
    Tree* right;
    Tree* left;
public:
    Tree() {}
    Tree(char op1, Tree* left, Tree* right)
    {
        if(DEBUG) printf("'%c'\n", op1);
        this -> op = op1;
        this -> left = left;
        this -> right = right;
    }
    ~Tree()
    {
        delete right;
        delete left;
    }
    virtual int value()
    {
        if (DEBUG) printf("op = %c\n", op);
        switch (op) {
            case '+':
                return left -> value() + right -> value();
                break;
            case '-':
                return left -> value() - right -> value();
                break;
            case '*':
                return left -> value() * right -> value();
                break;
            case '/':
                return left -> value() / right -> value();
                break;
            case '%':
                return left -> value() % right -> value();
                break;
            default:
                printf("What is that '%c'\n", op);
                perror("Unexpected char.");
                exit(1);
        }
    }
    virtual void toString()
    {
        printf("( ");
        left -> toString();
        printf(" '%c' ", op);
        right -> toString();
        printf(" )");
    }
};
               
class Leaf : public Tree
{
    int number;
public:
    Leaf(int number)
    {
        this -> number = number;
    }
    int value()
    {
        return number;
    }
    void toString()
    {
        printf("%d", number);
    }
};

stack<term> st = stack<term>();

Tree* execute()
{
    if(st.empty())
    {
        perror("Not enough terms.");
        exit(1);
    }
    if(DEBUG) printf("execute method.\n");
    term t;
    t = st.top();
    st.pop();
    if(t.isNumber)
    {
        if(DEBUG) printf("We read number.\n");
        return new Leaf(t.number);
    }
    else
    {
        if(DEBUG) printf("We read op.\n");
        Tree* right = execute();
        Tree* left = execute();
        if(DEBUG) printf("Generating tree.\n");
        return new Tree(t.op, left, right);
    }
}

int find_char(char* digits, int base, char c)
{
    for(int i = 0; i < base; i++)
    {
        if(*(digits + i) == c)
            return i;
    }
    
    return -1;
}

int read_number_ext(int base, char* digits, int* i, char* inp)
{
    int number = 0;
    
    int p;
    while(*i < MAX_L && (p = find_char(digits, base, tolower(inp[*i]))) != -1)
	{
		number *= base;
		number += p;
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
        else if(isdigit(c))
        {
            term t;
            t.number = read_number(&i, inp);
            t.isNumber = true;
            st.push(t);
        }
		else if(c == '-' && i + 1 < MAX_L && isdigit(inp[i + 1]))
        {
            i ++;
            term t;
            t.number = -read_number(&i, inp);
            t.isNumber = true;
            st.push(t);
        }
		else
		{
            if(c != '+' && c!='-' && c!='*' && c!='/' && c!='%')
            {
                printf("Unexpected character at position %d\n", i);
                perror("Unknown op.");  return 1;
            }
            if (DEBUG) {
                printf("Read '%c' \n", c);
            }
            term t;
            t.op = c;
            t.isNumber = false;
            st.push(t);
		}
	}
    
    Tree* tree = execute();
    
    printf("Result of the expression is %d\n", tree -> value());

    printf("Expression in infix form: \n");
    tree -> toString();
    printf("\n");
    
    free(inp);
    delete tree;

    return 0;
}
