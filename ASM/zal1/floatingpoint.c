#include <stdio.h>
#include <assert.h>
#include <float.h>

#define DEBUG 1

extern long plus (long arg1, long arg2);
extern long minus (long arg1, long arg2);
extern long times2 (long arg1, long arg2);
extern long divide (long arg1, long arg2);

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


void test3(int i, double b, double c)
{
    double d;
    if (DEBUG) printf ("tolong(b) = %ld\n", tolong(b));
    if (DEBUG) printf ("tolong(c) = %ld\n", tolong(c));
    printf ("Case %d: %lf, %lf\n",i, b, c);
    if (DEBUG) printf("My result long(b * c) = %ld\n", times2(tolong(b), tolong(c)));
    printf("My result b * c = %lf\n", d = fromlong(times2(tolong(b), tolong(c))));
    if (DEBUG) printf ("IEEE long(b * c) = %ld\n", tolong(b * c));
    if (DEBUG) printf ("IEEE b * c = %lf\n", b * c);
    assert(d == b * c);
}

void test4(int i, double b, double c)
{
    double d;
    if (DEBUG) printf ("tolong(b) = %ld\n", tolong(b));
    if (DEBUG) printf ("tolong(c) = %ld\n", tolong(c));
    printf ("Case %d: %lf, %lf\n",i, b, c);
    if (DEBUG) printf("My result long(b / c) = %ld\n", divide(tolong(b), tolong(c)));
    printf("My result b / c = %lf\n", d = fromlong(divide(tolong(b), tolong(c))));
    if (DEBUG) printf ("IEEE long(b / c) = %ld\n", tolong(b / c));
    if (DEBUG) printf ("IEEE b / c = %lf\n", b / c);
    assert(d == b / c);
}

int main()
{
    double b, c, d;
    test(0, 1, 1);
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
    test(29, DBL_MAX + 2, -DBL_EPSILON);
    test(30, DBL_MAX + 2, -DBL_MAX);
    test(31, DBL_MAX * 2, -DBL_EPSILON);
    test(32, DBL_MAX * 2, -DBL_MAX);
    test(33, DBL_MAX + 2, DBL_MAX * 2);
    test(34, DBL_MAX + 2, -DBL_MAX * DBL_MAX);
    
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
    test2(41, DBL_MAX + 2, -DBL_EPSILON);
    test2(42, DBL_MAX + 2, -DBL_MAX);
    test2(43, DBL_MAX * 2, -DBL_EPSILON);
    test2(44, DBL_MAX * 2, -DBL_MAX);
    test2(45, DBL_MAX + 2, DBL_MAX * 2);
    test2(46, DBL_MAX + 2, -DBL_MAX * DBL_MAX);
    
    test3(41, 2, 2);
    test3(42, 2, 1);
    test3(43, -2, 1);
    test3(44, -2, -10000);
    test3(45, 0, -20000);
    test3(46, 1, DBL_EPSILON);
    test3(47, 1, -DBL_EPSILON);
    test3(48, 0, DBL_EPSILON);
    test3(49, -DBL_EPSILON, DBL_EPSILON);
    test3(50, -DBL_MAX, DBL_MAX);
    test3(51, DBL_MAX, DBL_MAX);
    test3(52, DBL_MAX, 2);
    test3(53, -DBL_MAX, 2);
    test3(54, DBL_MAX, -2);
    test3(55, DBL_MAX, DBL_EPSILON);
    test3(56, -DBL_MAX, DBL_EPSILON);
    test3(57, 42342131, 0);
    test3(58, 123123123.012312, 1012999);
    test3(59, -123123, -123.01231256);
    test3(60, DBL_MAX + 2, -DBL_EPSILON);
    test3(61, DBL_MAX + 2, -DBL_MAX);
    test3(62, DBL_MAX * 2, -DBL_EPSILON);
    test3(63, DBL_MAX * 2, -DBL_MAX);
    test3(64, DBL_MAX + 2, DBL_MAX * 2);
    test3(65, DBL_MAX + 2, -DBL_MAX * DBL_MAX);
    
    test4(60, 3, 1);
    test4(61, 1, 2);
    test4(62, 4, 2);
    test4(63, -1000, -0.5);
    test4(64, 2, 2);
    test4(65, 2, 1);
    test4(66, -2, 1);
    test4(67, -2, -10000);
    test4(68, 0, -20000);
    test4(69, 1, DBL_EPSILON);
    test4(70, 1, -DBL_EPSILON);
    test4(71, 0, DBL_EPSILON);
    test4(72, -DBL_EPSILON, DBL_EPSILON);
    test4(73, -DBL_MAX, DBL_MAX);
    test4(74, DBL_MAX, DBL_MAX);
    test4(75, DBL_MAX, 2);
    test4(76, -DBL_MAX, 2);
    test4(77, DBL_MAX, -2);
    test4(78, DBL_MAX, DBL_EPSILON);
    test4(79, -DBL_MAX, DBL_EPSILON);
    test4(80, 42342131, 0);
    test4(81, 123123123.012312, 1012999);
    test4(82, -123123, -123.01231256);
    test4(80, 42342131, 0);
    test4(81, DBL_MAX + 2, -DBL_EPSILON);
    test4(82, DBL_MAX + 2, -DBL_MAX);
    test4(83, DBL_MAX * 2, -DBL_EPSILON);
    test4(84, DBL_MAX * 2, -DBL_MAX);
    test4(85, DBL_MAX + 2, DBL_MAX * 2);
    test4(86, DBL_MAX + 2, -DBL_MAX * DBL_MAX);
    test4(87, 0 + 2, -DBL_EPSILON);
    test4(88, 0 + 4, -DBL_MAX);
    test4(89, DBL_MAX * 2, -DBL_EPSILON * DBL_EPSILON);
    test4(90, DBL_MAX * 2, -DBL_MAX);
    test4(91, DBL_MAX + 2, DBL_MAX * 2);
    test4(92, DBL_MAX + 2, -DBL_MAX * DBL_MAX);
    test4(93, DBL_EPSILON, -DBL_MAX);
    return 0;
}