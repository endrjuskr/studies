#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <stdlib.h>

#define CHECK 1

struct timeval t1, t2;

/* Naiwne mnożenie macierzy kwadratowych A i B, wynik w C */

extern void optimal_mm(int size, float *a, float *b, float *c); 

#define ALIGN 16

void *aligned_malloc(int size) {
    void *mem = malloc(size+ALIGN+sizeof(void*));
    void **ptr = (void**)((long)(mem+ALIGN+sizeof(void*)) & ~(ALIGN-1));
    ptr[-1] = mem;
    return ptr;
}

void aligned_free(void *ptr) {
    free(((void**)ptr)[-1]);
}

int close_power_2(int size)
{
  int i = 4;
  while (i < size)
    i = i << 1;
  return i;
}


int main (int argc, char *argv[]) {
  float *A, *B, *C;
  int N, N_ext, M, i, j, errno;
#ifdef CHECK
  FILE *fd;
#endif

  if (argc != 3) {
    printf("Usage: mm-test matrix_size iter\n");
    exit(0);
  }

  N = atoi(argv[1]);
  M = atoi(argv[2]);

  N_ext = close_power_2(N);
  printf ("extended size = %d\n", N_ext);

  /* Alokacja i inicjowanie macierzy (alligned) */
  A = aligned_malloc(N_ext * N_ext * sizeof(float));
  B = aligned_malloc(N_ext * N_ext * sizeof(float));
  C = aligned_malloc(N_ext * N_ext * sizeof(float));
  

#ifdef CHECK
  if ((fd = fopen("tmp111", "r")) == NULL) {
     printf("Cannot open tmp111\n");
     exit(0);
  }
   
  for (i = 0; i < N; i++)
  {
    for (j = 0; j < N; j++)
      fscanf(fd, " %f", (A + i * N_ext + j));

    for (j = N; j < N_ext; j++)
      *(A + i * N_ext + j) = 0.0;
  }
  for(i = N; i < N_ext; i++)
    for (j = 0; j < N_ext; j++)
      *(A + i * N_ext + j) = 0.0;

  fclose(fd);

  if ((fd = fopen("tmp222", "r")) == NULL) {
     printf("Cannot open tmp222\n");
     exit(0);
  }
   
  for (i = 0; i < N; i++)
  {
    for (j = 0; j < N; j++)
      fscanf(fd, "%f", (B + i * N_ext + j));
    for (j = N; j < N_ext; j++)
      *(B + i * N_ext + j) = 0.0;
  }
  for(i = N; i < N_ext; i++)
    for (j = 0; j < N_ext; j++)
      *(B + i * N_ext + j) = 0.0;

  fclose(fd);
#else
  srand48(128);

  for (i = 0; i < N; i++)
  {
    for (j = 0; j < N; j++)
    {
      *(A + i * N_ext + j) = drand48();
      *(B + i * N_ext + j) = drand48();
    }
    for (j = N; j < N_ext; j++)
    {
      *(B + i * N_ext + j) = 0.0;
      *(A + i * N_ext + j) = 0.0;
    }
  }
  for(i = N; i < N_ext; i++)
    for (j = 0; j < N_ext; j++)
    {
      *(B + i * N_ext + j) = 0.0;
      *(A + i * N_ext + j) = 0.0;
    }

#endif

  /* Wielokrotne mnożenie */
  gettimeofday(&t1, NULL);
  for (i = 0; i < M; i++)
    optimal_mm(N_ext, B, A, C);
  gettimeofday(&t2, NULL);

  printf("Time for the optimal matrix multiplication is %d milliseconds\n",
         (t2.tv_sec - t1.tv_sec) * 1000 + 
         (t2.tv_usec - t1.tv_usec) / 1000);

#ifdef CHECK
  if ((fd = fopen("tmp333", "w")) == NULL) {
     printf("Cannot open tmp333\n");
     exit(0);
  }

  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++)
      fprintf(fd, "%6.2lf ", *(C + i * N_ext + j));
    fprintf(fd, "\n");
  }
  fclose(fd);
#endif

  aligned_free(A);
  aligned_free(B);
  aligned_free(C);

  return 0;
}
