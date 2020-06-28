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
//Constants
#define MAX_SOURCE_SIZE (0x100000)
#define MAX_DEVICE_SIZE 256

/* Flag set by ‘--verbose’. */
static int verbose_flag;
static struct option long_options[] =
{
    /* These options set a flag. */
    {"version",                 no_argument,            0, 'V'},
    {"kernel-program",          required_argument,      0, 'k'},
    {"opencode-answer",         required_argument,      0, 'o'},
    {"log",                     required_argument,      0, 'l'},
    {"help",                    no_argument,            0, 'h'},
    {"beton-amount",            required_argument,      0, 'a'},
    {"beton-amount-with-odds",  required_argument,      0, 'w'},
};

void help()
{
    printf("option\n");
    printf("-V, -version                     Show program version.\n");
    printf("-k, --kernel-program <path>      Path to opencl kernel program.\n");
    printf("-o, --opencode-answer <path>     Path to opencode anser csv path.\n");
    printf("-l, --log <path>                 Path to program runtime log.\n");
    printf("--beton-amount <path>            Path to bet amount csv path.\n");
    printf("--beton-amount-with-odds <path>  Path to bet amount with odds csv path.\n");
}

int loadArgs(int argc, char* argv[], 
        char kernel_program_path[], 
        char opencode_answer_path[], 
        char beton_amount_path[],
        char beton_amount_with_odds_path[],
        char log_dir[])
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
        
        case 'a':
            strcpy(beton_amount_path, optarg);
            break;

        case 'w':
            strcpy(beton_amount_with_odds_path, optarg);
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

void checkErr(cl_int err, const char* name)
{
    if(err != CL_SUCCESS)
    {
        printf("ERROR: %s ( %s )\n", name, err);
        exit(EXIT_FAILURE);
    }
}

void CL_CALLBACK contextCallback(const char * errInfo, const void * private_info, size_t cb, void * user_data)
{
    printf("Error occurred during context user: %s \n", errInfo);
    exit(EXIT_FAILURE);
}

void show_device_information(cl_device_id device)
{
    cl_uint addr_data;
    /* Extension data */
    char name_data[48], ext_data[4096];

    /* Access device name */
    cl_int err = clGetDeviceInfo(device, CL_DEVICE_NAME, 48 * sizeof(char), name_data, NULL);			
    if(err < 0) {		
        perror("Couldn't read extension data");
        exit(1);
    }

    /* Access device address size */
    clGetDeviceInfo(device, CL_DEVICE_ADDRESS_BITS, sizeof(addr_data), &addr_data, NULL);			

    /* Access device extensions */
    clGetDeviceInfo(device, CL_DEVICE_EXTENSIONS, 4096 * sizeof(char), ext_data, NULL);			
    
    printf("NAME: %s\nADDRESS_WIDTH: %u\nEXTENSIONS: %s\n", name_data, addr_data, ext_data);
}


int load_opencl_kernel_code_file(const char* kernel_code_path, char *source_str)
{
    FILE *fp;
    size_t source_size;

    fp = fopen(kernel_code_path, "r");
    if (!fp) {
        fprintf(stderr, "Failed to load kernel.\n");
        exit(1);
    }
    source_size = fread( source_str, 1, MAX_SOURCE_SIZE, fp);
    //printf(source_str);
    fclose( fp );
    
    return source_size;
}

cl_int GetGetPlatforms(cl_uint total_platforms, cl_platform_id **platforms)
{
    cl_int errNum;
    char* ext_data;
    size_t ext_size;

    //*platforms = (cl_platform_id*) malloc(sizeof(cl_platform_id) * total_platforms);
    errNum = clGetPlatformIDs(total_platforms, *platforms, NULL);
    checkErr((errNum != CL_SUCCESS)? errNum : (total_platforms <= 0 ? -1 : CL_SUCCESS), "clGetPlatFormIDs for get data.");
    
    int platformId = -1;
    for (platformId = 0; platformId < total_platforms; platformId++)
    {
        errNum = clGetPlatformInfo(*platforms[platformId], CL_PLATFORM_EXTENSIONS, 0, NULL, &ext_size);
        checkErr(errNum, "clGetPlatformInfo for init.");

        ext_data = (char*)malloc(ext_size);
        errNum = clGetPlatformInfo(*platforms[platformId], CL_PLATFORM_EXTENSIONS, ext_size, ext_data, NULL);
        checkErr(errNum, "clGetPlatformInfo for get data.");
        printf("Platform ID: %d\nsupports extensions: \n %s\n", platformId, ext_data); 
    }

    if(ext_data)
        free(ext_data);
    return errNum;
}

int GetDevices(cl_platform_id platform, cl_device_id** devices)
{
    cl_uint total_devices;
    int platformId = 0; 
    cl_int errNum = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 0, NULL, &total_devices);
    if (errNum != CL_SUCCESS && errNum != CL_DEVICE_NOT_FOUND)
    {
        checkErr(errNum, "clGetDeviceIDs");
    } 
    else if (total_devices > 0)
    {
        *devices = (cl_device_id *) malloc(sizeof(cl_device_id) * total_devices);
        errNum = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, total_devices, *devices, NULL);
        //checkErr(errNum, "clGetDeviceIDs");
        printf("found number of GPU : %d\n", total_devices);
    }
    else
    {
        printf("No CPU devices found.\n");
        exit(-1);
    }
    return total_devices;
}


int run_kernel_sum_beton_total_amount(cl_context context, cl_device_id device, cl_kernel kernel,
        int beton_length, int wgaer_length, 
        cl_int* mask, 
        cl_float* bet_amount, 
        cl_float** result)
{
    cl_command_queue queue = NULL;
    cl_int errNum;
    queue = clCreateCommandQueue(context, device, 0, &errNum);
    checkErr(errNum, "clCreateCommandQueue");
    
    /* Create a write-only buffer to hold the output data */
    cl_mem mask_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, 
        sizeof(cl_int) * beton_length, 
        mask, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a buffer");
      exit(1);   
    };
    cl_mem bet_amount_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, 
        sizeof(cl_float) * beton_length * wgaer_length, 
        bet_amount, 
        &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a buffer");
      exit(1);   
    };
    cl_mem result_buffer = clCreateBuffer(context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_float) * beton_length, 
        NULL, 
        &errNum);
     if(errNum < 0) {
      perror("Couldn't create a buffer");
      exit(1);   
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mask_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &bet_amount_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 2, sizeof(cl_mem), &result_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 3, sizeof(int), &wgaer_length);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };

    checkErr(errNum, "clSetKernelArg");
    printf("send input arguments memory to GPU ........... successful!!\n");

    int dim = 1;
    const size_t global_offset[] = { 0 };
    const size_t global_size[] = { beton_length };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL, NULL);

    checkErr(errNum, "clEnqueueNDRangeKernel");    
    printf("pass kernel code to GPU%d\n", 0);

    *result = (cl_float*)malloc(sizeof(cl_float) * beton_length);
    /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_float) * beton_length, *result, 0, NULL, NULL);
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(1);   
    }

    clReleaseMemObject(mask_buffer);
    clReleaseMemObject(bet_amount_buffer);
    clReleaseMemObject(result_buffer);
    clReleaseCommandQueue(queue);
    return 0;
}

int run_kernel_calc_numbers_risk(cl_context context, cl_device_id device, cl_kernel kernel,
        int beton_length, int opencode_length, 
        cl_float* total_beton_amount, 
        cl_float* total_beton_amount_with_odds, 
        cl_int* opencode_answer, 
        cl_float** result)
{
    cl_command_queue queue = NULL;
    cl_int errNum;
    queue = clCreateCommandQueue(context, device, 0, &errNum);
    checkErr(errNum, "clCreateCommandQueue");
    
    /* Create a write-only buffer to hold the output data */
    cl_mem total_beton_amount_buffer = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(cl_float) * beton_length, total_beton_amount, &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a buffer");
      exit(1);   
    };
    cl_mem total_beton_amount_with_odds_buffer = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(cl_float) * beton_length, total_beton_amount_with_odds, &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a buffer");
      exit(1);   
    };

    cl_mem opencode_answer_buffer = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, sizeof(cl_int) * beton_length * opencode_length, opencode_answer, &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a buffer");
      exit(1);   
    };
    cl_mem result_buffer = clCreateBuffer(context,CL_MEM_WRITE_ONLY ,sizeof(cl_float)* opencode_length, NULL, &errNum);
     if(errNum < 0) {
      perror("Couldn't create a buffer");
      exit(1);   
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &total_beton_amount_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &total_beton_amount_with_odds_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 2, sizeof(cl_mem), &opencode_answer_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 3, sizeof(cl_mem), &result_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 4, sizeof(int), &beton_length);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument");
        exit(1);   
    };

    checkErr(errNum, "clSetKernelArg");
    printf("send input arguments memory to GPU ........... successful!!\n");

    int dim = 1;
    const size_t global_offset[] = { 0 };
    const size_t global_size[] = { opencode_length };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL, NULL);

    checkErr(errNum, "clEnqueueNDRangeKernel");    
    printf("pass kernel code to GPU%d\n", 0);

    *result = (cl_float*)malloc(sizeof(cl_float) * opencode_length);
    /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_float) * opencode_length, *result, 0, NULL, NULL);
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(1);   
    }

    clReleaseMemObject(total_beton_amount_buffer);
    clReleaseMemObject(total_beton_amount_with_odds_buffer);
    clReleaseMemObject(opencode_answer_buffer);
    clReleaseMemObject(result_buffer);
    clReleaseCommandQueue(queue);
    return 0;
}

void readBetonAmountFromCsv(char* beton_amount_path, 
    int beton_length, int wager_length, 
    cl_float** beton_amount)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_bet_amount_index = 0;

    fp = fopen(beton_amount_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", fp);
        exit(EXIT_FAILURE);
    }
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;
            
        p = NULL;
        for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
        {
            float ret = strtof(p, NULL);
            *(*beton_amount + csv_bet_amount_index) = ret;
            csv_bet_amount_index ++;
        }
    }
    fclose(fp);
}

void readOpnecodeAnswerFromCsv(char* opencode_answer_path, 
    int beton_length, 
    int opencode_length, 
    cl_int** opencode_answer)
{
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
    //cl_int* a = (cl_int *)malloc(sizeof(cl_int) * 3628800 * 1056);

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
                    *(*opencode_answer + total_opencode_answer) = ret;
                    total_opencode_answer ++;
                }
            }
            else
            {
                //all beton
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
}

int main(int argc, char* argv[])
{
    char kernel_program_path[255];
    char opencode_answer_path[255];
    char beton_amount_path[255];
    char beton_amount_with_odds_path[255];
    char log_dir[255];
    strcpy(log_dir, "log/");

    loadArgs(argc, argv, 
        &kernel_program_path, 
        &opencode_answer_path, 
        &beton_amount_path,
        &beton_amount_with_odds_path,
        &log_dir);
    
    printf("kernel_program_file:%s\n", kernel_program_path);
    printf("opencode_answer_file:%s\n", opencode_answer_path);
    printf("beton_amount_path:%s\n", beton_amount_path);\
    printf("beton_amount_with_odds_path:%s\n", beton_amount_with_odds_path);
    printf("log_dir:%s\n", log_dir);
    
    cl_int errNum;
    cl_platform_id* platforms = NULL;
    cl_int total_platforms = 0;
    cl_device_id* devices = NULL;
    cl_context context = NULL;
    cl_command_queue queue;
    cl_program program = NULL;
    cl_kernel kernel_sum_beton_total_amount = NULL;
    cl_kernel kernel_calc_numbers_risk = NULL;
    int platformId = 0; 

    errNum = clGetPlatformIDs(0, NULL, &total_platforms);
    checkErr((errNum != CL_SUCCESS)? errNum : (total_platforms <= 0 ? -1 : CL_SUCCESS), "clGetPlatformIDs for init.");
    printf("get number of Platforms: %d\n", total_platforms);

    platforms = (cl_platform_id*) malloc(sizeof(cl_platform_id) * total_platforms);
    errNum = clGetPlatformIDs(total_platforms, platforms, NULL);
    checkErr((errNum != CL_SUCCESS)? errNum : (total_platforms <= 0 ? -1 : CL_SUCCESS), "clGetPlatFormIDs for get data.");
    printf("get all Platforms.\n");

    int total_devices = GetDevices(platforms[platformId], &devices);
    
    // show device info
    for(int deviceId = 0; deviceId < total_devices; deviceId++)
    {
        printf("==================== GPU%d ====================\n", deviceId);
        show_device_information(devices[deviceId]);
        printf("==============================================\n");
    }
    
    // Create an OpenCL context
    context = clCreateContext(NULL, total_devices, devices, &contextCallback, NULL, &errNum);
    checkErr(errNum, "clCreateContext");
    printf("create OpenCL context for all GPU ........... successful!!\n");

    // Load the kernel source code into the array source_str
    char* source_content = (char*)malloc(MAX_SOURCE_SIZE);
    size_t source_size = load_opencl_kernel_code_file(kernel_program_path, source_content);

    // Create a program from the kernel source
    program = clCreateProgramWithSource(context, 1, 
            (const char **)&source_content, (const size_t *)&source_size, &errNum);
    checkErr(errNum, "clCreateProgramWithSource");
    printf("create OpenCL program from %s ........... successful!!\n", kernel_program_path);
    if(source_content)
        free(source_content);

    // Build the program
    errNum = clBuildProgram(program, total_devices, devices, NULL, NULL, NULL);
    checkErr(errNum, "clBuildProgram");
    // 產出Build cl檔案的log不然cl程式碼寫錯也編譯不出來
    if(errNum < 0){
        // Shows the log
        char* build_log;
        size_t log_size;
        // First call to know the proper size
        clGetProgramBuildInfo(program, *devices, CL_PROGRAM_BUILD_LOG, 0, NULL, &log_size);
        build_log = malloc(log_size+1);
        // Second call to get the log
        clGetProgramBuildInfo(program, *devices, CL_PROGRAM_BUILD_LOG, log_size, build_log, NULL);
        build_log[log_size] = '\0';
        printf(build_log);
        if(build_log)
            free(build_log);
    }
    printf("build OpenCL program from %s .......... successful!!\n", kernel_program_path);
    
    // Create OpenCL Kernel program
    kernel_sum_beton_total_amount = clCreateKernel(program, "sum_beton_total_amount", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "sum_beton_total_amount");
    
    kernel_calc_numbers_risk = clCreateKernel(program, "calc_numbers_risk", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "calc_numbers_risk");
    
    int beton_length = 1056;
    int wager_length = 129;
    cl_int* mask = (cl_int*)malloc(sizeof(cl_int) * beton_length);
    cl_float* beton_amount = (cl_float*)malloc(sizeof(cl_float) * beton_length * wager_length);
    cl_float* beton_amount_with_odds = (cl_float*)malloc(sizeof(cl_float) * beton_length * wager_length);
    cl_float* total_beton_amount = NULL;
    cl_float* total_beton_amount_with_odds = NULL;
    cl_float* result = NULL;
    
    // fill mask content
    for(int i=0; i<=beton_length-1; i++)
    {
        mask[i] = 1;
    }
    readBetonAmountFromCsv(beton_amount_path, beton_length, wager_length, &beton_amount);
    run_kernel_sum_beton_total_amount(context, devices[0], kernel_sum_beton_total_amount, 
        beton_length, wager_length,
        mask, beton_amount, &total_beton_amount);

    float sum = 0;
    for(int i=0; i<=beton_length-1; i++)
    {
        sum += total_beton_amount[i];
    }
    printf("sum total_beton_amount = %f\n", sum);
    
    readBetonAmountFromCsv(beton_amount_with_odds_path, beton_length, wager_length, &beton_amount_with_odds);
    run_kernel_sum_beton_total_amount(context, devices[0], kernel_sum_beton_total_amount, 
        beton_length, wager_length,
        mask, beton_amount_with_odds, &total_beton_amount_with_odds);

    sum = 0;
    for(int i=0; i<=beton_length-1; i++)
    {
        sum += total_beton_amount_with_odds[i];
    }
    printf("sum total beton amount with odds = %f\n", sum);
    
    if(mask)
        free(mask);
    if(beton_amount)
        free(beton_amount);
    if(beton_amount_with_odds)
        free(beton_amount_with_odds);
   
    int opencode_length = 3628800;
    opencode_length = 20;
    cl_int* opencode_answer = (cl_int *)malloc(sizeof(cl_int) * opencode_length * beton_length);
    readOpnecodeAnswerFromCsv(opencode_answer_path, beton_length, opencode_length, &opencode_answer);
    run_kernel_calc_numbers_risk(context, devices[0], kernel_calc_numbers_risk, 
        beton_length, opencode_length, 
        total_beton_amount, 
        total_beton_amount_with_odds, 
        opencode_answer,
        &result);
   
    exit(EXIT_SUCCESS);
}