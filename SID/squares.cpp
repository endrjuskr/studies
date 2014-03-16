#include <cstdlib>
#include <cstdio>
#include <ctime>
#include <cstring>

#define N 30
#define LEVEL 7
#define SUFFIX 10

using namespace std;

int p = 59;
int q = 1000000007;
char* best_seq;
char* current;
char* tmp;
long long int  P[N];
long long int H[N+1][N+1];
long long int SQUARE[2*N];

void initP(int n) 
{
 P[0] = 1;
 for (int i = 1; i < n; ++i)
 {
  P[i] = P[i-1]*p % q;
 }
}

void countHashSufix(char* slowo, int n)
{
 H[n][n-1] = 0;
 for (int i = n-1; i >= 0; --i)
 {
  H[i][n-1] = (H[i+1][n-1]*p + (int)slowo[i]) % q;
 }
}

void countHash(int n)
{
 for (int i = 0; i < n; ++i)
 {
  for (int j = i+1; j < n; ++j)
  {
   H[i][j] = (H[i][n-1] - P[j-i+1]*H[j+1][n-1]) % q;
  }
 }
}

int score(char *word)
{
  int result = 0;
  int n = strlen(word);
  countHashSufix(word, n);
  countHash(n);
  for (int i = 0; i < n; ++i)
  {
    for (int j = i+1; j < n; j+=2)
    {
      int s = (i+j)/2;
      if (H[i][s] == H[s+1][j])
      {
        bool test = true;
        for (int k = i; k <= s; ++k)
        {
          test &= word[k] == word[k+s];
          if (!test) break;
        }
        for (int k = 0; k < result; ++k)
        {
          test &= SQUARE[k] != H[i][j];
          if (!test) break;
        }
        if (test)
        {
          SQUARE[result++] = H[i][j];
        }
      }
    }
 }
 return result;
}

void createSuffix(int n)
{
      int c = SUFFIX;
      while(c--)
      {
        tmp[N - 1 - c] = n % 2 + 1;
        n /= 2; 
      }
}

void finishCounting()
{
     int c = SUFFIX;
     int i = 1;
     while(c--) i*=2;
     tmp = (char*)malloc(N * sizeof(char));
     for(int k = 0; k < N - SUFFIX; k++)
      tmp[k] = best_seq[k];
     for(int k = N - SUFFIX; k < N; k++)
      tmp[k] = 1;
     for(int k = 1; k < i; k++)
     {
        createSuffix(k);
        if(score(tmp) > score(best_seq))
        {
            for(int j = 0; j < N; j++)
              best_seq[j] = tmp[j];
        }
     } 
}

void sample(int index)
{
     int size = N - index;
     for(int i = 0; i < size; i++)
     {
             current[i] = rand() % 2 + 1;
     }
}

void NMCS(int best, int size, int level)
{
  //printf("s - %d\n", size);
  //for (int i = 0; i < size; ++i)
  //  printf("%d", (int)current[i]);
  //printf("\n");
  //getchar();
  if (size >= N - SUFFIX)
  {
    return;
  }

   if (level == 0)
   {
      sample(size);
      return;
   }

     for(int i = 1; i <= 2; i++)
     {
       current[size + 1] = i;
       NMCS(0, size + 1, level - 1);      
       if (score(current) > best)
       {
          for(int k = 0; k < N; k++)
            best_seq[k] = current[k];
          best = score(current);
       }
     }
     //printf("%d %d\n", size, level);
     for(int k = 0; k < N; k++)
        current[k] = best_seq[k];

     if(level == LEVEL)
      NMCS(best, size + 1, level);
     return;
}

int main()
{
    srand (time(NULL));
    
    initP(N);
    
    best_seq = (char*)malloc(N * sizeof(char));
    current = (char*)malloc(N * sizeof(char));
    NMCS(0, 0, LEVEL);
    finishCounting();
    
    printf("Word:\n");
    for (int i = 0; i < N; ++i)
        printf("%d", (int)best_seq[i]);
    printf("\n");
    
    printf("Score: %d\n", score(best_seq));
    return 0;
}
