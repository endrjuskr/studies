#include <stdio.h>
#include <assert.h>
#include <float.h>

#define DEBUG 1

extern long plus (long arg1, long arg2);
extern long minus (long arg1, long arg2);
/*extern long times (long arg1, long arg2);
extern long diviide (long arg1, long arg2);
*/

const int s_sign = 63;
const int s_significant = 51;
const int s_exponent = 62;

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
    unsigned char * bit_representation = (unsigned char *) &l;
    /*int i, t = sizeof(double);
    for(i = t - 1; i >= sizeof(double) / 2; i--)
    {

        unsigned char tmp = bit_representation[i];
        bit_representation[i] = bit_representation[t - 1 - i];
        bit_representation[t - 1 - i] = tmp;
    }
    */
    double * result = (double *)bit_representation;
    return *result;
}

double fromlong2(long long l)
{
    double sign = 0.0;
    sign = -1 * ((l >> s_sign) & 1);
    if (sign == 0)
    {
        sign = 1.0;
    }

    double significant = 0.0;
    int i;
    for (i = 0; i <= s_significant; i++)
    {
        significant = significant / 2;
        significant = significant + ((l >> i) & 1);
    }
    significant = significant / 2;
    significant = significant + 1;
    
    if(DEBUG) printf("significant = %lf\n", significant);
    
    long long e = 2;
    long long exponent = 0.0;
    for (i = s_exponent; i > s_significant; i--)
    {
        exponent *= 2;
        exponent += ((l >> i) & 1);
    }

    i = exponent - 1023;
    exponent = 0.0;
    if(DEBUG) printf("Exp = %d\n", i);
    if (i == -1023)
    {
        if(DEBUG) printf ("Zero occured.\n");
        return sign * 0.0;
    }

    while (i > 0)
    {
        if((i & 1) == 1)
        {
            exponent += e;
        }

        e *= 2;
        i >>= 1;
    }

    if (exponent == 0)
    {
        exponent = 1.0;
    }

    return sign * significant * (double)exponent;
}

void test(int i, double b, double c)
{
    double d;
    if (DEBUG) printf ("tolong(b) = %ld\n", tolong(b));
    if (DEBUG) printf ("tolong(c) = %ld\n", tolong(c));
    printf ("Case %d: %lf, %lf\n",i, b, c);
    if (DEBUG) printf("My result long(b - c) = %ld\n", plus(tolong(b), tolong(c)));
    printf("%lf\n", d = fromlong(plus(tolong(b), tolong(c))));
    if (DEBUG) printf ("IEEE long(b + c) = %ld\n", tolong(b + c));
    if (DEBUG) printf ("IEEE b + c = %lf\n", b + c);
    assert(d == b + c);
}

void test2(int i, double b, double c)
{
    double d;
    if (DEBUG) printf ("tolong(b) = %ld\n", tolong(b));
    if (DEBUG) printf ("tolong(c) = %ld\n", tolong(c));
    printf ("Case %d: %lf, %lf\n",i, b, c);
    if (DEBUG) printf("My result long(b - c) = %ld\n", minus(tolong(b), tolong(c)));
    printf("My result b - c = %lf\n", d = fromlong(minus(tolong(b), tolong(c))));
    if (DEBUG) printf ("IEEE long(b - c) = %ld\n", tolong(b - c));
    if (DEBUG) printf ("IEEE b - c = %lf\n", b - c);
    assert(d == b - c);
}

int main()
{
    double b, c, d;
    test(1, 1, 2);
    test(2, 2, 2);
    test(3, 1.5, 2);
    test(4, 0, 2);
    test(5, 2, 0);
    test(6, 0, 0);
    test(7, 2, -2);
    test(8, -2, 2);
    test(9, -2, -2);
    test(10, DBL_MIN, 0);
    test(11, DBL_MIN, DBL_MAX / 2);
    test(12, DBL_MAX, DBL_MAX / 2);
    test(13, DBL_MAX, 0);
    test(14, DBL_MAX, DBL_EPSILON);
    test(15, DBL_MIN, DBL_MAX);
    test(16, DBL_MIN, -DBL_MIN);
    test(17, DBL_MAX, -2);
    test(18, DBL_EPSILON, DBL_EPSILON);
    test(19, DBL_EPSILON, -DBL_EPSILON);
    test2(20, 2, 2);
    test2(21, DBL_MAX, DBL_EPSILON);
    test2(22, DBL_MAX, -DBL_MAX / 2);
    return 0;
}