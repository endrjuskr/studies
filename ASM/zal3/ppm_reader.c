#include <netpbm/pam.h>
#include <stdbool.h>
#include <stdint.h>
 
int main(int argc, char **argv){
  FILE * ppm_file = fopen(argv[1]);
  struct pam inpam;
  tuple *tuplerow;
  unsigned int row;

  pm_init(argv[0], 0);

  pnm_readpaminit(ppm_file, &inpam, PAM_STRUCT_SIZE(tuple_type));

  tuplerow = pnm_allocpamrow(&inpam);

  for(row = 0; row < inpam.height; row++){
    unsigned int column;
    pnm_readpamrow(&inpam, tuplerow);
    for(column = 0; column < inpam.width; ++column){
      unsigned long *pixel = tuplerow[column];
      printf("%ld\n", pixel[0]);
    }
  }
  pnm_freepamrow(tuplerow);
  fclose(ppm_file);
  return 0;
}