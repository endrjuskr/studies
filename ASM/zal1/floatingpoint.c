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
    test(18, DBL_MAX, -DBL_MAX);
    test(19, DBL_MAX, -DBL_MAX/2);
    test(20, DBL_MAX, -DBL_MAX/4);
    test(21, DBL_MAX, -DBL_MAX/8);
    test(22, DBL_MAX, -DBL_MAX/16);
    test(23, DBL_MAX, -DBL_MAX/100000);
    test(24, DBL_MAX, -DBL_MAX/2048);
    test(25, DBL_MAX, -DBL_MAX/128);
    test(26, DBL_MAX, -DBL_MAX/127);
    test(27, DBL_EPSILON, DBL_EPSILON);
    test(28, DBL_EPSILON, -DBL_EPSILON);
    test2(29, 2, 2);
    test2(30, 2, -2);
    test2(31, -4, -2);
    test2(32, -111, -DBL_EPSILON);
    test2(33, -111, DBL_MAX);
    test2(34, -111, DBL_MIN);
    test2(35, DBL_MAX, DBL_EPSILON);
    test2(36, DBL_MAX, DBL_MIN / 2);
    test2(37, DBL_MAX, DBL_MAX);
    test2(38, DBL_MAX, -DBL_MAX);
    test2(39, DBL_MAX, -(DBL_MAX / 2));
    test2(40, DBL_MAX, (DBL_MAX / 2));
    return 0;
}