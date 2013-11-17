#include <stdio.h>

/*extern long plus (long arg1, long arg2);
extern long minus (long arg1, long arg2);
extern long times (long arg1, long arg2);
extern long diviide (long arg1, long arg2);
*/

const int s_sign = 63;
const int s_base = 51;
const int s_exp = 62;

long tolong(double l)
{
    long result  = 0;
    unsigned char * bit_representation = (unsigned char *) &l;
    int i;
    for(i = sizeof(double) - 1; i >= 0; i--)
    {
        result = result * 16 * 16;
        result += (long)bit_representation[i];
    }
    return result;	
}

double fromlong(long long l)
{
    double result = 0.0;
    result = -1 * ((l >> s_sign) & 1);
    if (result == 0)
    {
        result = 1.0;
    }

    double base = 0.0;
    int i;
    for (i = 0; i <= s_base; i++)
    {
        base = base / 2;
        base = base + ((l >> i) & 1);
    }
    base = base / 2;
    base = base + 1;
    printf("Base = %lf\n", base);
    long long e = 0;
    long long ex = 0.0;
    for (i = s_exp; i > s_base; i--)
    {
        e *= 2;
        e += ((l >> i) & 1);
    }
    i = e - 1023;
    e = 2;
    printf("Exp = %d\n", i);
    while (i > 0)
    {
        if((i & 1) == 1)
        {
            ex += e;
        }
        e *= 2;
        i >>= 1;
    }

    if (ex == 0)
    {
        ex = 1.0;
    }

    return result * base * (double)ex;
}

int main()
{
    double b;
    scanf("%lf", &b);
    printf("Long repr - %ld\n", tolong(b));
    printf("Back to double - %.20lf\n", fromlong(tolong(b)));
    return 0;
}
