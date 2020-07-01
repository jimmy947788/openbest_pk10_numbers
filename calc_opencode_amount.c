
#include "common/Common.h"
#include "common/hashmap.h"

int run_kernel_sum_beton_total_amount(
        cl_context context, 
        cl_command_queue queue, 
        cl_kernel kernel,
        int beton_length, int wgaer_length, 
        cl_ushort* one_mask, 
        cl_float* bet_amount, 
        cl_float** result)
{
    cl_int errNum;
  
    /* Create a write-only buffer to hold the output data */
    cl_mem mask_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, 
        sizeof(cl_ushort) * beton_length, 
        one_mask, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a mask_buffer");
      exit(1);   
    };
    cl_mem bet_amount_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, 
        sizeof(cl_float) * beton_length * wgaer_length, 
        bet_amount, 
        &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a bet_amount_buffer");
      exit(1);   
    };
    cl_mem result_buffer = clCreateBuffer(context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_float) * beton_length, 
        NULL, 
        &errNum);
     if(errNum < 0) {
      perror("Couldn't create a result_buffer");
      exit(1);   
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mask_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(mask_buffer)");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &bet_amount_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(bet_amount_buffer)");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 2, sizeof(cl_mem), &result_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(result_buffer)");
        exit(1);   
    };
    errNum = clSetKernelArg(kernel, 3, sizeof(cl_int), &wgaer_length);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(wgaer_length)");
        exit(1);   
    };

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
    //clReleaseCommandQueue(queue);
    return 0;
}

int run_kernel_calc_numbers_risk(
        cl_context context, 
        cl_command_queue queue, 
        cl_kernel kernel,
        int beton_length, int opencode_length, 
        cl_float* total_beton_amount, 
        cl_float* total_beton_amount_with_odds, 
        cl_short* opencode_answer, 
        cl_float** result)
{
    cl_int errNum;
    
    /* Create a write-only buffer to hold the output data */
    cl_mem total_beton_amount_buffer = clCreateBuffer(
        context, 
        CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, 
        sizeof(cl_float) * beton_length, 
        total_beton_amount, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a total_beton_amount_buffer");
      exit(1);   
    };
    
    cl_mem total_beton_amount_with_odds_buffer = clCreateBuffer(
        context, 
        CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, 
        sizeof(cl_float) * beton_length, 
        total_beton_amount_with_odds, 
        &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a total_beton_amount_with_odds_buffer");
      exit(1);   
    };

    cl_mem opencode_answer_buffer = clCreateBuffer(
        context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_short) * beton_length * opencode_length, 
        opencode_answer, 
        &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a opencode_answer_buffer");
      exit(1);   
    };

    cl_mem result_buffer = clCreateBuffer(
        context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_float) * opencode_length , 
        NULL, 
        &errNum);
    if(errNum < 0) {
      perror("Couldn't create a result_buffer");
      exit(1);   
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &total_beton_amount_buffer);
    checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (total_beton_amount_buffer)");
        exit(1);   
    };

    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &total_beton_amount_with_odds_buffer);
    checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (total_beton_amount_with_odds_buffer)");
        exit(1);   
    };

    errNum = clSetKernelArg(kernel, 2, sizeof(cl_mem), &opencode_answer_buffer);
    checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (opencode_answer_buffer)");
        exit(1);   
    };

    errNum = clSetKernelArg(kernel, 3, sizeof(cl_mem), &result_buffer);
    checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (sub_opencode_answer_buffer)");
        exit(1);   
    };

    errNum = clSetKernelArg(kernel, 4, sizeof(cl_int), &beton_length);
    checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (beton_length)");
        exit(1);   
    };

    int dim = 1;
    const size_t global_offset[] = { 0 };
    const size_t global_size[] = { opencode_length };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL, NULL);

    checkErr(errNum, "clEnqueueNDRangeKernel");    
    printf("pass kernel code to GPU%d\n", 0);

    /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_float) * opencode_length, *result, 0, NULL, NULL);
    checkErr(errNum, "clEnqueueReadBuffer");
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(1);   
    }

    clReleaseMemObject(total_beton_amount_buffer);
    clReleaseMemObject(total_beton_amount_with_odds_buffer);
    clReleaseMemObject(opencode_answer_buffer);
    clReleaseMemObject(result_buffer);
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
    map_t mymap;
    mymap = hashmap_new();

    LoadArgs(argc, argv, 
        &kernel_program_path, 
        &opencode_answer_path, 
        &beton_amount_path,
        &beton_amount_with_odds_path,
        &log_dir);
    
    if(strlen(kernel_program_path) == 0 || strlen(opencode_answer_path) == 0)
    {
        printf("must be support argument...\n");
        printf("\t--kernel-program <path>\n");
        printf("\t--opencode-answer <path>\n");
        printf("show help\n");
        printf("\tcalc_opencode_amount -h\n");
        exit(EXIT_SUCCESS);
    }
    
#ifdef DEBUG
    printf("kernel_program_file:%s\n", kernel_program_path);
    printf("opencode_answer_file:%s\n", opencode_answer_path);
    printf("beton_amount_path:%s\n", beton_amount_path);
    printf("beton_amount_with_odds_path:%s\n", beton_amount_with_odds_path);
    printf("log_dir:%s\n", log_dir);
#endif

    int betonLength = 0, opencodeLength = 0; 
    int wager_length = 129; 
    cl_device_id* deviceList = NULL;
    cl_context context = NULL;
    cl_program* program = NULL;
    cl_uint total_devices = 0;
    cl_short* opencode_answer = NULL;
    cl_command_queue* queueList = NULL;
    cl_float* opencode_answer_result = NULL;
    cl_ushort* one_mask = NULL;
    cl_float* beton_amount = NULL;
    cl_float* beton_amount_with_odds = NULL;
    cl_float* total_beton_amount = NULL;
    cl_float* total_beton_amount_with_odds = NULL;
    char** opencodeList  = NULL;
    // 儲存時間用的變數
    clock_t timeStart, timeEnd;

    printf("load opencode answer length ");
    GetDataLength(opencode_answer_path, &opencodeLength, &betonLength);
    printf("...........(opencode Length:%d, beton Length:%d)\n",opencodeLength, betonLength);

    printf("load opencode answer from csv ");
    timeStart = clock();
    opencode_answer = (cl_short *)malloc(sizeof(cl_short) * betonLength * opencodeLength);
    opencodeList =  (char**)malloc(sizeof(*opencodeList) * opencodeLength);
    ReadOpnecodeAnswerFromCsv(opencode_answer_path, &opencode_answer, &opencodeList);
    printf("........... successful !! (time:%fs)\n",  (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
    timeEnd = clock();
 
    printf("opencode[3]=%s\n", opencodeList[3]);
    printf("opencode[%d]=%s\n", opencodeLength -1,  opencodeList[opencodeLength-1]);

    printf("alloc opencode_answer_result array (length: %d)", opencodeLength);
    opencode_answer_result = (cl_float*)malloc(sizeof(cl_float) * opencodeLength);
    printf("........... successful !!\n");
    
    printf("alloc one_mask array (length: %d)", betonLength);
    one_mask = (cl_ushort*)malloc(sizeof(cl_ushort) * betonLength);
     // fill mask content
    for(int i=0; i<=betonLength-1; i++) 
    {
        one_mask[i] = 1;
    }
    printf("........... successful !!\n");

    total_devices = GetDevices(&deviceList);

    // Create an OpenCL context
    printf("create OpenCL context for all GPU");
    context = clCreateContext(NULL, total_devices, deviceList, &contextCallback, NULL, &errNum);
    checkErr(errNum, "clCreateContext");
    printf(" ........... successful!!\n");

     // Create an OpenCL queue
    printf("create OpenCL queue for all GPU");
    queueList = (cl_command_queue*)malloc(sizeof(cl_command_queue) * total_devices);
    for(int i=0; i<=total_devices -1; i++ )
    {
        queueList[i] = clCreateCommandQueue(context, deviceList[i], 0, &errNum);
        checkErr(errNum, "clCreateCommandQueue");
    }
    printf(" ........... successful!!\n");

    printf("build OpenCL program from");
    // Create an OpenCL program
    BuildKernelProgram(kernel_program_path, context, total_devices, deviceList, &program);
    printf(".......... successful!!\n");

    // Create OpenCL Kernel program
    cl_kernel kSumBetonTotalAmount = clCreateKernel(program, "sum_beton_total_amount", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "sum_beton_total_amount");
    
    cl_kernel kCalcNumbersRisk = clCreateKernel(program, "calc_numbers_risk", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "calc_numbers_risk");

    printf("release OpenCL program");
    clReleaseProgram(program);
    printf(".......... successful!!\n");

    //以下重複直行
    //===================================================================================================
#ifdef DEBUG
    float sum = 0;
#endif
    beton_amount = (cl_float*)malloc(sizeof(cl_float) * betonLength * wager_length);
    ReadBetonAmountFromCsv(beton_amount_path, &beton_amount);
    total_beton_amount = (cl_float*)malloc(sizeof(cl_float) * betonLength);
    timeStart = clock();;
    run_kernel_sum_beton_total_amount(context, queueList[0], kSumBetonTotalAmount, 
        betonLength, wager_length,
        one_mask, beton_amount, &total_beton_amount);
    timeEnd = clock();;
    printf("run_kernel_sum_beton_total_amount... time:%fs\n", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC ); 

    if(beton_amount)
        free(beton_amount);

#ifdef DEBUG
    sum = 0;
    for(int i=0; i<=betonLength-1; i++)
    {
        sum += total_beton_amount[i];
    }
    printf("====> sum total_beton_amount = %f\n", sum);
#endif

    beton_amount_with_odds = (cl_float*)malloc(sizeof(cl_float) * betonLength * wager_length);
    ReadBetonAmountFromCsv(beton_amount_with_odds_path, &beton_amount_with_odds);
    total_beton_amount_with_odds = (cl_float*)malloc(sizeof(cl_float) * betonLength);

    timeStart = clock();;
    run_kernel_sum_beton_total_amount(context, queueList[0], kSumBetonTotalAmount, 
        betonLength, wager_length,
        one_mask, beton_amount_with_odds, &total_beton_amount_with_odds);
    timeEnd = clock();;
    printf("run_kernel_sum_beton_total_amount... time:%fs\n", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC ); 
    
    if(beton_amount_with_odds)
        free(beton_amount_with_odds);

#ifdef DEBUG
    sum = 0;
    for(int i=0; i<=betonLength-1; i++)
    {
        sum += total_beton_amount_with_odds[i];
    }
    printf("====> sum total beton amount with odds = %f\n", sum);
#endif

    timeStart = clock();;
    memset(opencode_answer_result, 0, opencodeLength);
    run_kernel_calc_numbers_risk(context, queueList[0], kCalcNumbersRisk, 
        betonLength, opencodeLength, 
        total_beton_amount, 
        total_beton_amount_with_odds, 
        opencode_answer,
        &opencode_answer_result);
    timeEnd = clock();;
    printf("run_kernel_calc_numbers_risk... time:%fs\n", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC ); 

    if(total_beton_amount)
        free(total_beton_amount);
    if(total_beton_amount_with_odds)
        free(total_beton_amount_with_odds);
    /*
    int error;
    data_struct_t* value;
    for(int i=0; i<= opencodeLength -1; i++){
        value = malloc(sizeof(data_struct_t));
        strcpy(value->opencode, opencodeList[i]);
        value->amount = (float)opencode_answer_result[i];
        error = hashmap_put(mymap,  value->opencode, value);
    }*/


#ifdef DEBUG
    for(int i=0; i<=opencodeLength - 1; i++)
    {
        printf("opencode_answer_result[%d]=%f \n", i, opencode_answer_result[i]);
    }
#endif

    exit(EXIT_SUCCESS);
}