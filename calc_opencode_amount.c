#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <getopt.h>

#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#if !defined(ARRAY_SIZE)
    #define ARRAY_SIZE(x) (sizeof((x)) / sizeof((x)[0]))
#endif

#define VERSION "1.00"

/* Flag set by ‘--verbose’. */
static int verbose_flag;
static struct option long_options[] =
{
    /* These options set a flag. */
    {"version",               no_argument,       0, 'V'},
    {"kernel-program",   required_argument,      0, 'k'},
    {"opencode-answer",  required_argument,      0, 'o'},
    {"log",              required_argument,      0, 'l'},
    {"help",                  no_argument,       0, 'h'},
};

void help()
{
    printf("option\n");
    printf("-V, -version                   Show program version.\n");
    printf("-k, --kernel-program <path>    Path to opencl kernel program.\n");
    printf("-o, --opencode-answer <path>   Path to opencode anser csv path.\n");
    printf("-l, --log <path>               Path to program runtime log.\n");
}

int loadArgs(int argc, char* argv[], char kernel_program_path[], char opencode_answer_path[], char log_dir[])
{
    int cmd_opt;
    while(1) {
        /* getopt_long stores the option index here. */
        int option_index = 0;

        cmd_opt = getopt_long (argc, argv, "vk:o:l:h", /* v不用帶參數, k:必須要帶參數 a:必須要帶參數 h不用帶參數 l:必須要帶參數 */
                       long_options, &option_index);   
        /* Detect the end of the options. */
        if (cmd_opt == -1) {
            break;
        }

        switch (cmd_opt)
        {
        case 'V':
            printf("Version:%s\n", VERSION);
            exit(EXIT_SUCCESS);

        case 'k':
            strcpy(kernel_program_path, optarg);
            break;

        case 'o':
            strcpy(opencode_answer_path, optarg);
            break;

        case 'l':
            strcpy(log_dir, optarg);
            break;

        case 'h':
            help();
            exit(EXIT_SUCCESS);

        case '?':
            /* getopt_long already printed an error message. */
            break;

        default:
            abort ();
        }
    } 
}

int main(int argc, char* argv[])
{
    char kernel_program_path[255];
    char opencode_answer_path[255];
    char log_dir[255];
    strcpy(log_dir, "log/");

    loadArgs(argc, argv, &kernel_program_path, &opencode_answer_path, &log_dir);
    
    printf("kernel_program_file:%s\n", kernel_program_path);
    printf("opencode_answer_file:%s\n", opencode_answer_path);
    printf("log_dir:%s\n", log_dir);
    printf("asdasd\n");
    
    
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_column_index = 0;
    int csv_row_index = 0;
    int row_index = 0;
    long long total_opencode_answer = 0;
    cl_int* a = (cl_int *)malloc(sizeof(cl_int) * 3628800 * 1056);


    fp = fopen(opencode_answer_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", fp);
        exit(EXIT_FAILURE);
    }

    char* opencode = "1-2-3-4-5-6-7-8-9-10";
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;
            
        p = NULL;
        csv_column_index = 0;
        for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
        {
            if(csv_row_index >=1){
                if(csv_column_index == 0){
                    printf("opencode:%s\n", p);
                }
                else
                {
                    int ret = strtol(p, NULL, 10);
                    a[total_opencode_answer] = ret;
                    total_opencode_answer ++;
                }
            }
            else
            {
                opencode = p;
                printf("%s\n", opencode);
            }
            csv_column_index ++;
            
        }
        csv_row_index++;
        //printf("%s", line);
    }

    fclose(fp);
    if (line)
        free(line);

    printf( "Enter a value :");
    int c = getchar( );
    
    exit(EXIT_SUCCESS);
}