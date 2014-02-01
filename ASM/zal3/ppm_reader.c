/* Andrzej Skrodzki as292510.
   Programowanie w Asemblerze - zadanie 3. */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

extern void convert_ppm(int*, int, int, int, int);

int main(int argc, char **argv){
  if (argc != 5)
  {
     printf("Usage - original_file destination_file color_component color_change.\n");
     return 1;
  }
  FILE * ppm_file = fopen(argv[1], "r");
  FILE * converted_ppm_file = fopen(argv[2], "w+");
  
  if(ppm_file == NULL)
  {
    printf("Cannot open original file.\n");
    return 1;
  }
  
  if(converted_ppm_file == NULL)
  {
    printf("Cannot open destination file.\n");
    return 1;
  }
  
  int color_component = atoi(argv[3]);
  int color_change = atoi(argv[4]);
  printf("%d %d\n", color_component, color_change);
  int * image_array;
  int width, height, max_size;
  unsigned char c;
  // Wczytaj typ
  while((c = fgetc(ppm_file)) != '\n');
  fprintf(converted_ppm_file, "P6\n");
  while((c = fgetc(ppm_file)) != '\n');
  fprintf(converted_ppm_file, "#Modified file by as292510.\n");
  fscanf(ppm_file, "%d %d\n", &width, &height);
  printf("%d %d\n", width, height);
  fprintf(converted_ppm_file, "%d %d\n", width, height);
  fscanf(ppm_file, "%d\n", &max_size);
  printf("%d\n", max_size); 
  if(color_component > 3 || color_component < 1)
  {
    printf("Wrong color component number. It should be between 1 and 3.\n");
    return 1;
  }
  
  fprintf(converted_ppm_file, "%d\n", max_size);
  image_array = (int *)malloc(sizeof(int) * width * height * 3);
  int i, j;
  for (i = 0; i < height; i++)
  {
    for(j = 0; j < width; j++)
    {
      int current_component = i * (width * 3) + j * 3;
      fread(&c, 1, 1, ppm_file);
      image_array[current_component] = c;
      fread(&c, 1, 1, ppm_file);
      image_array[current_component + 1] = c;
      fread(&c, 1, 1, ppm_file);
      image_array[current_component + 2] = c;
    }
  }
  printf("end of file\n");
  for(i = 0; i<width * height * 3; i++)
  {
    assert(image_array[i] >= 0);
  }
  
  // Color component to 1, 2 lub 3 ale w convert_ppm uzywamy prostego dodawania wiec tutaj juz przesuniemy.
  convert_ppm(image_array, width, height, color_component - 1, color_change);
  
  for(i = 0; i<width * height * 3; i++)
  {
    assert(image_array[i] >= 0);
  }
  
  for(i = 0; i<width * height * 3; i++)
  {
    c = (unsigned char)image_array[i];
    fwrite(&c, sizeof(unsigned char), 1, converted_ppm_file);
  }
  
  fclose(ppm_file);
  fclose(converted_ppm_file);
  return 0;
}