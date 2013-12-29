#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#define CHECK 1 

struct timeval t1, t2;

/* Naiwne mnożenie macierzy kwadratowych A i B, wynik w C */

void naive_mm (int size, float *a, float *b, float *c) {
  int i, j, k;

  for (i = 0; i < size; i++)
    for (j = 0; j < size; j++) {
      *(c + i * size + j) = 0.0;
      for (k = 0; k < size; k++)
      {
        *(c + i * size + j) +=  *(a + i * size + k) * *(b + k * size + j);
      }
    }
}


int main (int argc, char *argv[]) {
  float *A, *B, *C;
  int N, M, i, j;
#ifdef CHECK
  FILE *fd;
#endif

  if (argc != 3) {
    printf("Usage: mm-test matrix_size iter\n");
    exit(0);
  }

  N = atoi(argv[1]);
  M = atoi(argv[2]);

  /* Alokacja i inicjowanie macierzy */
  A = (float *)malloc(N * N * sizeof(float));
  B = (float *)malloc(N * N * sizeof(float));
  C = (float *)malloc(N * N * sizeof(float));
#ifdef CHECK
  if ((fd = fopen("tmp111", "r")) == NULL) {
     printf("Cannot open tmp111\n");
     exit(0);
  }
   
  for (i = 0; i < N; i++)
    for (j = 0; j < N; j++)
      fscanf(fd, "%f", (A + i * N + j));
  fclose(fd);

  if ((fd = fopen("tmp222", "r")) == NULL) {
     printf("Cannot open tmp222\n");
     exit(0);
  }
   
  for (i = 0; i < N; i++)
    for (j = 0; j < N; j++)
      fscanf(fd, " %f", (B + i * N + j));
  fclose(fd);
#else
  srand48(100);

  for (i = 0; i < N * N; ++i) {
    A[i] = drand48();
    B[i] = drand48();
  }
#endif

  /* Wielokrotne mnożenie */
  gettimeofday(&t1, NULL);
  for (i = 0; i < M; i++)
    naive_mm(N, B, A, C);
  gettimeofday(&t2, NULL);

  printf("Time for the matrix multiplication is %d milliseconds\n",
         (t2.tv_sec - t1.tv_sec) * 1000 + 
         (t2.tv_usec - t1.tv_usec) / 1000);

#ifdef CHECK
  if ((fd = fopen("tmp333", "w")) == NULL) {
     printf("Cannot open tmp333\n");
     exit(0);
  }

  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++)
      fprintf(fd, "%6.2lf ", *(C + i * N + j));
    fprintf(fd, "\n");
  }
  fclose(fd);
#endif

  return 0;
}
