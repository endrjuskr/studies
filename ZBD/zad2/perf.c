#include <stdio.h>
#include <sys/time.h>
#include <stdlib.h>
#include <time.h>

#define BLOCK_SIZE 1024 * 8 // rozmiar bloku, czyli 8kB

#define READ 1

struct timeval t1, t2;

int main(int argc, char** argv)
{
	// Podajemy w pierwszym argumencie nazwe pliku.
	// W drugim podajemy liczbe testow.
	// W trzecim podajemy rozmiar pliku w bajtach.
	if (argc != 4)
	{
		printf("Wrong usage.\n");
		return -1;
	}

	FILE * fd;
	char* data;

	fd = fopen(argv[1], "r+");
	if (fd == NULL)
	{
		printf("Cannot open a file.\n");
		return -1;
	}

	fseek(fd, 0L, SEEK_END);
	int file_size = ftell(fd);

	int block_count = atoi(argv[3]);
	srand (time(NULL));
	data = (char*)malloc(sizeof(char) * BLOCK_SIZE * block_count);

	file_size -= block_count * BLOCK_SIZE;

	int test_count = atoi(argv[2]);
	int operation_number_in_test;
	int i, picked_block;
	for(i = 1; i <= test_count; i++)
	{
		operation_number_in_test = 0;
		int t = 200000;
		gettimeofday(&t1, NULL);
		while (t--)
		{
			picked_block = drand48();
			fseek(fd, picked_block, SEEK_SET);
			#ifdef READ
			fgets(data, BLOCK_SIZE * block_count, fd);
			#else
			fgets(data, fd);
			#endif
			operation_number_in_test++;
		}

		gettimeofday(&t2, NULL);
		double sec_diff = (t2.tv_sec - t1.tv_sec) * 1000 + (t2.tv_usec - t1.tv_usec) / 1000;
		printf("%lf\n", sec_diff);
		printf("Test %d - %d operations.\n", i, (int)((double)operation_number_in_test / sec_diff));
	}
	
	fclose(fd);
	return 0;
}