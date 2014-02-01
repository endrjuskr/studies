#include <stdio.h>
#include <sys/time.h>
#include <stdlib.h>
#define BLOCK_SIZE 1024 * 8 // rozmiar bloku, czyli 8kB

#define READ 1

struct timeval t1, t2;

int main(int argc, char** argv)
{
	// Podajemy w pierwszym argumencie nazwe pliku.
	// W drugim podajemy liczbe testow.
	// W trzecim podajemy rozmiar pliku w bajtach.
	// W czwartym podajemy rozmiar bloku, ktory wczytujemy
	if (argc != 5)
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

	int block_count = atoi(argv[4]);
	srand (time(NULL));
	data = (char*)malloc(sizeof(char) * BLOCK_SIZE * block_count);

	int test_count = atoi(argv[2]);
	int file_size = atoi(argv[3]);
	file_size -= block_count * BLOCK_SIZE;
	int operation_number_in_test;
	int i, picked_block;
	for(i = 1; i <= test_count; i++)
	{
		operation_number_in_test = 0;
		int milsec = 0;
		int t;
		do
		{
			operation_number_in_test++;gettimeofday(&t1, NULL);
			t = 1000;
			while (t--)
			{
				picked_block = drand48();
				fseek(fd, picked_block, SEEK_SET);
				//#ifdef READ
				fgets(data, BLOCK_SIZE * block_count, fd);
			//#else
			//fputs(data, fd);
			//#endif
			}
			printf("1\n");
			gettimeofday(&t2, NULL);
			milsec += (t2.tv_sec - t1.tv_sec) * 1000000 + (t2.tv_usec - t1.tv_usec);
		} while (milsec < 1000000);
		printf("Test %d - %d operations.\n", i, operation_number_in_test);
	}
	
	fclose(fd);
	return 0;
}