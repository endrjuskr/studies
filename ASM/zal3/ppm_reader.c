#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main(int argc, char **argv){
  FILE * ppm_file = fopen(argv[1], "r");
  FILE * converted_ppm_file = fopen(argv[2], "w+");
  int color_component = atoi(argv[3]);
  int color_change = atoi(argv[4]);
  int * image_array;
  char * line;
  size_t len = 1028;
  ssize_t read = 0;
  int width;
  int height;
  int max_size;
  // Wczytaj typ
  getline(&line, &len, ppm_file);
  fprintf(converted_ppm_file, "P3\n");
  getline(&line, &len, ppm_file);
  fprintf(converted_ppm_file, "%s", line);
  fscanf(ppm_file, "%d %d\n", &width, &height);
  printf("%d %d\n", width, height);
  fprintf(converted_ppm_file, "%d %d\n", width, height);
  fscanf(ppm_file, "%d\n", &max_size);
  printf("%d\n", max_size); 
  fprintf(converted_ppm_file, "%d\n", max_size);
  image_array = (int *)malloc(sizeof(int) * width * height);
  unsigned char c;
  int tmp;
  int i, j;
  for (i = 0; i < height; i++)
  {
    for(j = 0; j < width; j++)
    {
      int current_component = i * (width * 3) + j * 3;
      fread(&c, 1, 1, ppm_file);
      printf("1 - %d\n", (int)c);
      image_array[current_component] = (int)c;
      fread(&c, 1, 1, ppm_file);
      printf("2- %d\n", (int)c);
      image_array[current_component + 1] = (int)c;
      fread(&c, 1, 1, ppm_file);
      printf("3 - %d\n", (int)c);
      image_array[current_component + 2] = (int)c;
    }
  }
  printf("end of file\n");
  for(i = 0; i<width * height * 3; i++)
  {
    printf("%d\n", image_array[i]);
    assert(image_array[i] >= 0);
  }
  for(i = 0; i<width * height * 3; i++)
  {
    fprintf(converted_ppm_file, "%d\n", image_array[i]);
  }
  fclose(ppm_file);
  fclose(converted_ppm_file);
  return 0;
}