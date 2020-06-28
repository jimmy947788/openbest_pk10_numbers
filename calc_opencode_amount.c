
#include "common/Common.h"


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

int main(int argc, char* argv[])
{
    cl_int errNum;
    
    char kernel_program_path[255] = "";
    char opencode_answer_path[255] = "";
    char beton_amount_path[255] = "";
    char beton_amount_with_odds_path[255] = "";
    char log_dir[255];
    strcpy(log_dir, "log/");

    bool isBreak = LoadArgs(argc, argv, 
        &kernel_program_path, 
        &opencode_answer_path, 
        &beton_amount_path,
        &beton_amount_with_odds_path,
        &log_dir);
    
    if(isBreak)
        exit(EXIT_SUCCESS);
    if(strlen(kernel_program_path) == 0 || strlen(opencode_answer_path) == 0)
    {
        printf("must be support argument...\n");
        printf("\t--kernel-program <path>\n");
        printf("\t--opencode-answer <path>\n");
        printf("show help\n");
        printf("\tcalc_opencode_amount -h\n");
        exit(EXIT_SUCCESS);
    }
    
#ifdef _DEBUG
    printf("kernel_program_file:%s\n", kernel_program_path);
    printf("opencode_answer_file:%s\n", opencode_answer_path);
    printf("beton_amount_path:%s\n", beton_amount_path);
    printf("beton_amount_with_odds_path:%s\n", beton_amount_with_odds_path);
    printf("log_dir:%s\n", log_dir);
#endif

    int betonLength = 0, opencodeLength = 0; 
    int wager_length = 129; 
    cl_device_id* devices = NULL;
    cl_context context = NULL;
    cl_program* program = NULL;
    cl_uint total_devices = 0;
    cl_int* opencode_answer = NULL;

    printf("load opencode answer length...\n");
    GetDataLength(opencode_answer_path, &opencodeLength, &betonLength);
    printf("opencode Length:%d, beton Length:%d\n",opencodeLength, betonLength);

    opencode_answer = (cl_int *)malloc(sizeof(cl_int) * betonLength * opencodeLength);
    ReadOpnecodeAnswerFromCsv(opencode_answer_path, &opencode_answer);
 
    total_devices = GetDevices(&devices);

    // Create an OpenCL context
    context = clCreateContext(NULL, total_devices, devices, &contextCallback, NULL, &errNum);
    checkErr(errNum, "clCreateContext");
    printf("create OpenCL context for all GPU ........... successful!!\n");

    BuildKernelProgram(kernel_program_path, context, total_devices, devices, &program);

    // Create OpenCL Kernel program
    cl_kernel kSumBetonTotalAmount = clCreateKernel(program, "sum_beton_total_amount", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "sum_beton_total_amount");
    
    cl_kernel kCalcNumbersRisk = clCreateKernel(program, "calc_numbers_risk", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "calc_numbers_risk");

    cl_int* mask = (cl_int*)malloc(sizeof(cl_int) * betonLength);
    // fill mask content
    for(int i=0; i<=betonLength-1; i++)
    {
        mask[i] = 1;
    }

    //以下重複直行
    //===================================================================================================
    cl_float* beton_amount = (cl_float*)malloc(sizeof(cl_float) * betonLength * wager_length);
    cl_float* beton_amount_with_odds = (cl_float*)malloc(sizeof(cl_float) * betonLength * wager_length);
    cl_float* total_beton_amount = NULL;
    cl_float* total_beton_amount_with_odds = NULL;
    cl_float* result = NULL;
    
    ReadBetonAmountFromCsv(beton_amount_path, &beton_amount);
    total_beton_amount = (cl_float*)malloc(sizeof(cl_float) * betonLength);
    run_kernel_sum_beton_total_amount(context, devices[0], kSumBetonTotalAmount, 
        betonLength, wager_length,
        mask, beton_amount, &total_beton_amount);

    float sum = 0;
    for(int i=0; i<=betonLength-1; i++)
    {
        sum += total_beton_amount[i];
    }
    printf("sum total_beton_amount = %f\n", sum);
    
    ReadBetonAmountFromCsv(beton_amount_with_odds_path, &beton_amount_with_odds);
    total_beton_amount_with_odds = (cl_float*)malloc(sizeof(cl_float) * betonLength);
    run_kernel_sum_beton_total_amount(context, devices[0], kSumBetonTotalAmount, 
        betonLength, wager_length,
        mask, beton_amount_with_odds, &total_beton_amount_with_odds);

    sum = 0;
    for(int i=0; i<=betonLength-1; i++)
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
   
    run_kernel_calc_numbers_risk(context, devices[0], kCalcNumbersRisk, 
        betonLength, opencodeLength, 
        total_beton_amount, 
        total_beton_amount_with_odds, 
        opencode_answer,
        &result);
    
    for(int i=0; i<=20; i++)
    {
        printf("result[%d]=%f,", i, result[i]);
    }
    printf("\n");
    exit(EXIT_SUCCESS);
}