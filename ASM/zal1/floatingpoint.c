#include <stdio.h>

/*extern long plus (long arg1, long arg2);
extern long minus (long arg1, long arg2);
extern long times (long arg1, long arg2);
extern long diviide (long arg1, long arg2);
*/

const long sign = 1 << 3;
const long mantis = 0;
const long expon = 0;

long tolong(double l)
{
    long result  = 0;
    unsigned char * bit_representation = (unsigned char *) &l;
    int i;
    for(i = sizeof(double) - 1; i >= 0; i--)
    {
        result = result * 16 * 16;
        result += (double)bit_representation[i];
    }
    return result;	
}

double fromlong(long l)
{
    double result = 0.0;
    unsigned char * bit_representation = (unsigned char *) &l;
    return result;
}

int main()
{
    double b;
    scanf("%lf", &b);
    printf("%ld\n", tolong(b));
    printf("%ld\n", sign);
    return 0;
}
