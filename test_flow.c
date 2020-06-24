#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#if !defined(ARRAY_SIZE)
    #define ARRAY_SIZE(x) (sizeof((x)) / sizeof((x)[0]))
#endif

int main(void)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_column_index = 0;
    int row_index = 0;
    long long total_opencode_answer = 0;
    cl_int* a = (cl_int *)malloc(sizeof(cl_int) * 3628800 * 1056);

    char* filename = "/home/jimmywu/Developer/projects/openbest_pk10_numbers/data/opencode_table_all.csv";
    printf("filename: %s\n", filename);

    fp = fopen(filename, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", fp);
        exit(EXIT_FAILURE);
    }

    char* opencode = "1-2-3-4-5-6-7-8-9-10";
    printf("read = %ld\n", read);
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        //printf("total_opencode_answer=%ld\n", total_opencode_answer);
        //if( total_opencode_answer >= ((3628800 * 1056) -1))
        //    break;
        if (opencode == "10-9-8-7-6-5-4-3-2-1")
            break;
            
        p = NULL;
        csv_column_index = 0;
        for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
        {
            if(csv_column_index >=1){
                a[total_opencode_answer] = (int)p;
                total_opencode_answer ++;
            }
            else
            {
                opencode = p;
                printf("%s\n", opencode);
            }
            csv_column_index ++;
            
        }
        printf("\n");
        //printf("%s", line);
    }

    fclose(fp);
    if (line)
        free(line);

    printf( "Enter a value :");
    int c = getchar( );

    exit(EXIT_SUCCESS);
}