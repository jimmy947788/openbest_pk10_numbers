
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
    clock_t timeStart, timeEnd;
    timeStart = clock();
  
    printf("clCreateBuffer mask_buffer\n");
    /* Create a write-only buffer to hold the output data */
    cl_mem mask_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_ushort) * beton_length, 
        one_mask, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a mask_buffer");
      exit(EXIT_FAILURE);
    };

    printf("clCreateBuffer bet_amount_buffer\n");
    cl_mem bet_amount_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_float) * beton_length * wgaer_length, 
        bet_amount, 
        &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a bet_amount_buffer");
      exit(EXIT_FAILURE);
    };

    cl_mem result_buffer = clCreateBuffer(context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_float) * beton_length, 
        NULL, 
        &errNum);
     if(errNum < 0) {
      perror("Couldn't create a result_buffer");
      exit(EXIT_FAILURE);
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &mask_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(mask_buffer)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &bet_amount_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(bet_amount_buffer)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 2, sizeof(cl_mem), &result_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(result_buffer)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 3, sizeof(cl_int), &wgaer_length);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(wgaer_length)");
        exit(EXIT_FAILURE);
    };

    int dim = 1;
    const size_t global_offset[] = { 0 };
    const size_t global_size[] = { beton_length };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL,  NULL);

    checkErr(errNum, "clEnqueueNDRangeKernel");    
    printf("pass kernel code to GPU%d\n", 0);

     /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_float) * beton_length, *result, 0, NULL, NULL);
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(EXIT_FAILURE);
    }

    clReleaseMemObject(result_buffer);
    clReleaseMemObject(mask_buffer);
    clReleaseMemObject(bet_amount_buffer);
   
    timeEnd = clock();
    printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
    return 0;
}

int run_kernel_calc_numbers_risk(
        cl_context context, 
        cl_command_queue queue, 
        cl_kernel kernel,
        int beton_length, int opencode_length, int offset,
        cl_float* total_beton_amount, 
        cl_float* total_beton_amount_with_odds, 
        cl_mem* opencode_answer_table_buffer,
        cl_float** result)
{
    cl_int errNum;
    clock_t timeStart, timeEnd;
    timeStart = clock();
    
    /* Create a write-only buffer to hold the output data */
    cl_mem total_beton_amount_buffer = clCreateBuffer(
        context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_float) * beton_length, 
        total_beton_amount, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a total_beton_amount_buffer");
      exit(EXIT_FAILURE);
    };
    
    cl_mem total_beton_amount_with_odds_buffer = clCreateBuffer(
        context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_float) * beton_length, 
        total_beton_amount_with_odds, 
        &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a total_beton_amount_with_odds_buffer");
      exit(EXIT_FAILURE);
    };

    cl_buffer_region region;
    region.origin = offset;
    region.size = sizeof(cl_short) * beton_length * opencode_length;
    cl_mem sub_opencode_answer_table_buffer = clCreateSubBuffer(
        *opencode_answer_table_buffer, 
        CL_MEM_READ_ONLY , 
        CL_BUFFER_CREATE_TYPE_REGION, 
        &region, 
        &errNum);
   if(errNum < 0) {
      perror("Couldn't create a sub-buffer");
      exit(EXIT_FAILURE);
   }
    
#ifdef DEBUG
    void *main_buffer_mem = NULL, *sub_buffer_mem = NULL;
    size_t main_buffer_size, sub_buffer_size;
   /* Obtain size information about the buffers */
   clGetMemObjectInfo(*opencode_answer_table_buffer, CL_MEM_SIZE, 
         sizeof(main_buffer_size), &main_buffer_size, NULL);
   clGetMemObjectInfo(sub_opencode_answer_table_buffer, CL_MEM_SIZE, 
         sizeof(sub_buffer_size), &sub_buffer_size, NULL);
   printf("Main buffer size: %lu\n", main_buffer_size);
   printf("Sub-buffer size:  %lu\n", sub_buffer_size);
   
   /* Obtain the host pointers */
   clGetMemObjectInfo(*opencode_answer_table_buffer, CL_MEM_HOST_PTR, sizeof(main_buffer_mem), 
  	      &main_buffer_mem, NULL);
   clGetMemObjectInfo(sub_opencode_answer_table_buffer, CL_MEM_HOST_PTR, sizeof(sub_buffer_mem), 
  	      &sub_buffer_mem, NULL);
   printf("Main buffer memory address: %p\n", main_buffer_mem);
   printf("Sub-buffer memory address:  %p\n", sub_buffer_mem);
#endif

    cl_mem result_buffer = clCreateBuffer(
        context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_float) * opencode_length , 
        NULL, 
        &errNum);
    if(errNum < 0) {
      perror("Couldn't create a result_buffer");
      exit(EXIT_FAILURE);
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &total_beton_amount_buffer);
    //checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (total_beton_amount_buffer)");
        exit(EXIT_FAILURE);
    };

    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &total_beton_amount_with_odds_buffer);
    //checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (total_beton_amount_with_odds_buffer)");
        exit(EXIT_FAILURE);
    };

    errNum = clSetKernelArg(kernel, 2, sizeof(cl_mem), &sub_opencode_answer_table_buffer);
   // checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (sub_opencode_answer_table_buffer)");
        exit(EXIT_FAILURE);
    };

    errNum = clSetKernelArg(kernel, 3, sizeof(cl_mem), &result_buffer);
    //checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (result_buffer)");
        exit(EXIT_FAILURE);
    };

    errNum = clSetKernelArg(kernel, 4, sizeof(cl_int), &beton_length);
    //checkErr(errNum, "clSetKernelArg");
    if(errNum < 0) {
        perror("Couldn't set a kernel argument (beton_length)");
        exit(EXIT_FAILURE);
    };

    int dim = 1;
    const size_t global_offset[] = { 0 };
    const size_t global_size[] = { opencode_length };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL, NULL);

    printf("pass kernel code to GPU%d\n", 0);

    /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_float) * opencode_length, *result, 0, NULL, NULL);
    //checkErr(errNum, "clEnqueueReadBuffer");
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(EXIT_FAILURE);
    }

    clReleaseMemObject(total_beton_amount_buffer);
    clReleaseMemObject(total_beton_amount_with_odds_buffer);
    clReleaseMemObject(sub_opencode_answer_table_buffer);
    clReleaseMemObject(result_buffer);

    timeEnd = clock();
    printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
    return 0;
}

int run_kernel_find_best_amount_count(
        cl_context context, 
        cl_command_queue queue, 
        cl_kernel kernel,
        cl_float** opencode_amount_list,
        int amount_length,
        float amount_range1, float amount_range2,
        cl_uint* count_result)
{
    cl_int errNum;
    clock_t timeStart, timeEnd;
    timeStart = clock();

    /* Create a write-only buffer to hold the output data */
    cl_mem opencode_amount_list_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_float) * amount_length, 
        opencode_amount_list, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a opencode_amount_list_buffer");
      exit(EXIT_FAILURE);
    };

    cl_mem result_buffer = clCreateBuffer(
        context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_uint) , 
        NULL, 
        &errNum);
    if(errNum < 0) {
      perror("Couldn't create a result_buffer");
      exit(EXIT_FAILURE);
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &opencode_amount_list_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(opencode_amount_list_buffer)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &result_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(result_buffer)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 2, sizeof(float), &amount_range1);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(amount_range1)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 3, sizeof(float), &amount_range2);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(amount_range2)");
        exit(EXIT_FAILURE);
    };

    int dim = 1;
    const size_t global_offset[] = { 0 };
    const size_t global_size[] = { amount_length };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL, NULL);

    checkErr(errNum, "clEnqueueNDRangeKernel");    
    printf("pass kernel code to GPU%d\n", 0);

    /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_uint) , count_result, 0, NULL, NULL);
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(EXIT_FAILURE);
    }

    clReleaseMemObject(opencode_amount_list_buffer);
    clReleaseMemObject(result_buffer);

    timeEnd = clock();
    printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
    return 0;
}

int run_kernel_find_best_amount(
        cl_context context, 
        cl_command_queue queue, 
        cl_kernel kernel,
        cl_float** opencode_amount_list,
        int amount_length,
        int best_amount_count,
        float amount_range1, float amount_range2,
        cl_uint** result)
{
    cl_int errNum;
    clock_t timeStart, timeEnd;
    timeStart = clock();
  
    /* Create a write-only buffer to hold the output data */
    cl_mem opencode_amount_list_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_float) * amount_length, 
        opencode_amount_list, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a opencode_amount_list_buffer");
      exit(EXIT_FAILURE);
    };

    cl_mem result_counter_buffer = clCreateBuffer(context, 
        CL_MEM_WRITE_ONLY, 
        sizeof(cl_int), 
        NULL, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a best_amount_count_buffer");
      exit(EXIT_FAILURE);
    };

    cl_mem result_buffer = clCreateBuffer(
        context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_uint) * best_amount_count, 
        NULL, 
        &errNum);
    if(errNum < 0) {
      perror("Couldn't create a result_buffer");
      exit(EXIT_FAILURE);
    };

    cl_mem mutex_buffer = clCreateBuffer(context, 
        CL_MEM_WRITE_ONLY, 
        sizeof(cl_int), 
        NULL, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a mutex_buffer");
      exit(EXIT_FAILURE);
    };

    /* Create kernel argument */
    errNum = clSetKernelArg(kernel, 0, sizeof(cl_mem), &opencode_amount_list_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(opencode_amount_list_buffer)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 1, sizeof(cl_mem), &result_counter_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(result_counter_buffer)");
        exit(EXIT_FAILURE);
    };
    
    errNum = clSetKernelArg(kernel, 2, sizeof(cl_mem), &result_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(result_buffer)");
        exit(EXIT_FAILURE);
    };
    
    errNum = clSetKernelArg(kernel, 3, sizeof(cl_mem), &mutex_buffer);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(mutex_buffer)");
        exit(EXIT_FAILURE);
    };

    errNum = clSetKernelArg(kernel, 4, sizeof(float), &amount_range1);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(amount_range1)");
        exit(EXIT_FAILURE);
    };
    errNum = clSetKernelArg(kernel, 5, sizeof(float), &amount_range2);
    if(errNum < 0) {
        perror("Couldn't set a kernel argument(amount_range2)");
        exit(EXIT_FAILURE);
    };

    int dim = 1;
    const size_t global_offset[] = { 0 };
    const size_t global_size[] = { amount_length };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL, NULL);

    checkErr(errNum, "clEnqueueNDRangeKernel");    
    printf("pass kernel code to GPU%d\n", 0);

    /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_uint) * best_amount_count , *result, 0, NULL, NULL);
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(EXIT_FAILURE);
    }

    clReleaseMemObject(opencode_amount_list_buffer);
    clReleaseMemObject(result_counter_buffer);
    clReleaseMemObject(result_buffer);
    clReleaseMemObject(mutex_buffer);

    timeEnd = clock();
    printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
    return 0;
}

int create_socket()
{
    int sockfd = 0, ret = 0;
    sockfd = socket(AF_INET , SOCK_STREAM , 0);
    if (sockfd == -1){
        printf("Fail to create a socket.");
        exit(EXIT_FAILURE); 
    }
    //socket的連線
    struct sockaddr_in serverInfo;
    bzero(&serverInfo,sizeof(serverInfo));

    serverInfo.sin_family = PF_INET;
    serverInfo.sin_addr.s_addr = INADDR_ANY;
    serverInfo.sin_port = htons(SOCKET_PORT);
    ret = bind(sockfd,(struct sockaddr *)&serverInfo,sizeof(serverInfo));
    if(ret == -1)
    {
        printf("bind error. (%d)", ret);
        exit(EXIT_FAILURE); 
    }
    ret = listen(sockfd, 5);
    if(ret == -1)
    {
        printf("listen error. (%d)", ret);
        exit(EXIT_FAILURE); 
    }
    return sockfd;
}

int main(int argc, char* argv[])
{
    cl_int errNum;
    
    char kernel_program_file[MAX_LENGTH] = "";
    char opencode_answer_table_file[MAX_LENGTH] = "";
    char beton_amount_table_file[MAX_LENGTH] = "";
    char beton_amount_table_with_odds_file[MAX_LENGTH] = "";
    char current_path[MAX_LENGTH];
    char log_dir[MAX_LENGTH];
    strcpy(log_dir, "log/");
    //map_t mymap;
    //mymap = hashmap_new();

    LoadArgs(argc, argv, 
        &kernel_program_file, 
        &opencode_answer_table_file,
        &log_dir);
    
    if(strlen(kernel_program_file) == 0 || strlen(opencode_answer_table_file) == 0)
    {
        printf("must be support argument...\n");
        printf("\t--kernel-program <path>\n");
        printf("\t--opencode-answer <path>\n");
        printf("show help\n");
        printf("\tcalc_opencode_amount -h\n");
        exit(EXIT_SUCCESS);
    }
    
    getcwd( current_path, MAX_LENGTH );
#ifdef DEBUG
    printf("kernel_program_file:%s\n", kernel_program_file);
    printf("opencode_answer_table_file:%s\n", opencode_answer_table_file);
    printf("log_dir:%s\n", log_dir);
    printf("Current working dir: %s\n", current_path);
#endif

    int total_platforms = 0;
    cl_platform_id* platforms = NULL;
    int total_devices = 0;
    cl_device_id* device_list = NULL;
    cl_context context = NULL;
    cl_program* program = NULL;
    cl_command_queue* queue_list = NULL;

    int beton_Length = 0;
    uint32 opencode_Length = 0; 
    int wager_length = 0; 
    char expectId[MAX_LENGTH];
    cl_short* opencode_answer_table = NULL;
    cl_ushort* one_mask = NULL;
    cl_float* beton_amount_table = NULL;
    cl_float* beton_amount_with_odds_table = NULL;
    cl_float* total_beton_amount_vector = NULL;
    cl_float* total_beton_amount_with_odds_vector = NULL;
    char** opencodeList  = NULL;
    //資料分段數量
    int dataSegmentNum = 2;
    //分段儲存結果
    cl_float* opencode_answer_table_result1 = NULL;
    cl_float* opencode_answer_table_result2 = NULL;

    printf("get OpenCL platforms");
    total_platforms = get_platforms(&platforms);
    printf(" ........... successful!!(total_platforms=%d)\n", total_platforms);

    printf("create OpenCL GPU devices");
    total_devices = create_gpu_device_list(platforms[0], &device_list);
    printf(" ........... successful!!(total_devices=%d)\n", total_devices);

    // Create an OpenCL context
    printf("create OpenCL context for all GPU");
    context = clCreateContext(NULL, total_devices, device_list, &contextCallback, NULL, &errNum);
    checkErr(errNum, "clCreateContext");
    printf(" ........... successful!!\n");

    printf("create OpenCL command queue for all devics\n");
    create_queue_list(context, device_list, total_devices, &queue_list);
    printf(" ........... successful!!(total command queue=%d)\n", total_devices);

    printf("build OpenCL program from");
    // build an OpenCL program
    build_program_for_all_devices(kernel_program_file, context, device_list, &program);
    printf(".......... successful!!\n");

    // Create OpenCL Kernel function
    cl_kernel kSumBetonTotalAmount = clCreateKernel(program, "sum_beton_total_amount", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "sum_beton_total_amount");
    
    cl_kernel kCalcNumbersRisk = clCreateKernel(program, "calc_numbers_risk", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "calc_numbers_risk");

    cl_kernel kFindBestAmountCount = clCreateKernel(program, "find_best_amount_count", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "find_best_amount_count");

    cl_kernel kFindBestAmount = clCreateKernel(program, "find_best_amount", &errNum);
    checkErr(errNum, "clCreateKernel");
    printf("Create OpenCL Kernel program :%s\n", "find_best_amount");

    // release OpenCL program
    printf("release OpenCL program");
    clReleaseProgram(program);
    printf(".......... successful!!\n");
    //============================================================================
    printf("get opencode answer table shape...\n");
    get_opnecode_answer_table_shape(opencode_answer_table_file, &beton_Length, &opencode_Length);
    printf("opencode Length:%ld, beton Length:%d\n", opencode_Length, beton_Length);
    
    printf("load opencode answer table from csv...\n");
    fflush(stdout); //不給\n就不給輸出,flush強制輸出
    opencode_answer_table = (cl_short *)malloc(sizeof(cl_short) * beton_Length * opencode_Length);
    opencodeList = (char**)malloc(sizeof(*opencodeList) * opencode_Length);
    load_opnecode_answer_table(opencode_answer_table_file, &opencode_answer_table, &opencodeList);

    one_mask = (cl_ushort*)malloc(sizeof(cl_ushort) * beton_Length);
    for(int i=0; i<=beton_Length-1; i++ )
    {
        one_mask[i] = 1;
    }

    //以下重複直行
    //===================================================================================================
    int dataSegmentLength =  opencode_Length / dataSegmentNum;
    int dataSegmentOffset = 0;

    printf("alloc opencode_answer_table_result array (length: %d)", dataSegmentLength);
    opencode_answer_table_result1 = (cl_float*)malloc(sizeof(cl_float) * dataSegmentLength);
    opencode_answer_table_result2 = (cl_float*)malloc(sizeof(cl_float) * dataSegmentLength);
    printf("........... successful !!\n");
    
    //create opencode_answer_table Buffer
   cl_mem opencode_answer_table_buffer = clCreateBuffer(
        context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_short) * beton_Length * opencode_Length, 
        opencode_answer_table, 
        &errNum);    
    if(errNum < 0) {
        perror("Couldn't create a opencode_answer_table_buffer");
        exit(EXIT_FAILURE);
    };

    char recv_buffer[MAX_BUFFER_SIZE] = {};
    char* send_buffer = NULL;
    int forClientSockfd = 0, sockfd = 0;
    struct sockaddr_in clientInfo;
    int addrlen = sizeof(clientInfo);
    char dateTime[_DATETIME_SIZE];

    sockfd = create_socket();
    //cl_uint* result = NULL;
    float target_amount_range1 = 0;
    float target_amount_range2 = 0;
    float target_amount = 0;
    float tolerance = 0;
    //while 重複直行
    //===================================================================================================
    while(true)
    {
        forClientSockfd = accept(sockfd,(struct sockaddr*) &clientInfo, &addrlen);
        memset(recv_buffer, '\0', MAX_BUFFER_SIZE);
        recv(forClientSockfd, recv_buffer, sizeof(recv_buffer), 0);
        printf("======> %s\n", recv_buffer);
        load_socket_data(recv_buffer, 
            beton_amount_table_file, 
            beton_amount_table_with_odds_file, 
            &wager_length, 
            expectId,
            &target_amount,
            &tolerance);
        printf("beton_amount_table_file = %s\n", beton_amount_table_file);
        printf("beton_amount_table_with_odds_file = %s\n", beton_amount_table_with_odds_file);
        printf("wager_length = %d\n", wager_length);
        printf("expectId = %s\n", expectId);
        printf("target_amount = %f\n", target_amount);
        printf("tolerance = %f\n", tolerance);
        
        target_amount_range1 = target_amount - tolerance;
        target_amount_range2 = target_amount + tolerance;
        printf("target_amount_range1 = %f, target_amount_range2= %f \n", target_amount_range1, target_amount_range2);

#ifdef DEBUG
        float sum = 0;
#endif
        beton_amount_table = (cl_float*)malloc(sizeof(cl_float) * beton_Length * wager_length);
        load_beton_amount_table(beton_amount_table_file, &beton_amount_table);
        total_beton_amount_vector = (cl_float*)malloc(sizeof(cl_float) * beton_Length);
        run_kernel_sum_beton_total_amount(
            context, 
            queue_list[0], 
            kSumBetonTotalAmount, 
            beton_Length, wager_length,
            one_mask, beton_amount_table,
            &total_beton_amount_vector);
        if(beton_amount_table)
            free(beton_amount_table);
#ifdef DEBUG
        sum = 0;
        for(int i=0; i<=beton_Length-1; i++)
        {
            sum += total_beton_amount_vector[i];
        }
        printf("====> sum total_beton_amount = %f\n", sum);
#endif

        beton_amount_with_odds_table = (cl_float*)malloc(sizeof(cl_float) * beton_Length * wager_length);
        load_beton_amount_table(beton_amount_table_with_odds_file, &beton_amount_with_odds_table);
        total_beton_amount_with_odds_vector = (cl_float*)malloc(sizeof(cl_float) * beton_Length);
        run_kernel_sum_beton_total_amount(
            context, 
            queue_list[0], 
            kSumBetonTotalAmount, 
            beton_Length, wager_length,
            one_mask, beton_amount_with_odds_table, 
            &total_beton_amount_with_odds_vector);
        if(beton_amount_with_odds_table)
            free(beton_amount_with_odds_table);
#ifdef DEBUG
        sum = 0;
        for(int i=0; i<=beton_Length-1; i++)
        {
            sum += total_beton_amount_with_odds_vector[i];
        }
        printf("====> sum total beton amount with odds = %f\n", sum);
#endif
        //計算獎號開出金額 1/2
        //===================================================================
        printf("calc total win/loss amount in opencode list ... 1/2\n");
        dataSegmentOffset = 0;
        memset(opencode_answer_table_result1, 0.0f, dataSegmentLength);
        run_kernel_calc_numbers_risk(context, queue_list[0], kCalcNumbersRisk, 
            beton_Length, dataSegmentLength , dataSegmentOffset,
            total_beton_amount_vector, 
            total_beton_amount_with_odds_vector,  
            &opencode_answer_table_buffer,
            &opencode_answer_table_result1);
        clFinish(queue_list[0]);
#ifdef DEBUG
        for(int i=0; i<=20 - 1; i++)
        {
            printf("%s, result[%d]=%f \n", opencodeList[i], i, opencode_answer_table_result1[i]);
        }
#endif
        //計算獎號開出金額 2/2
        //====================================================================
        printf("calc total win/loss amount in opencode list ... 2/2\n");
        dataSegmentOffset = 1814400;
        memset(opencode_answer_table_result2, 0.0f, dataSegmentLength);
        run_kernel_calc_numbers_risk(context, queue_list[0], kCalcNumbersRisk, 
            beton_Length, dataSegmentLength,  dataSegmentOffset,
            total_beton_amount_vector, 
            total_beton_amount_with_odds_vector, 
            &opencode_answer_table_buffer,
            &opencode_answer_table_result2);
        clFinish(queue_list[0]);
#ifdef DEBUG
        for(int i=0; i<=20 - 1; i++)
        {
            printf("%s, result[%d]=%f \n",opencodeList[i +dataSegmentOffset ], i + dataSegmentOffset, opencode_answer_table_result2[i]);
        }
#endif
        // 過濾指定金額 1/2
        //====================================================================
        printf("count opencode when win/loss amount in range ... 1/2\n");
        int result_count = 0;
        run_kernel_find_best_amount_count(
            context, 
            queue_list[0],
            kFindBestAmountCount,
            opencode_answer_table_result1,
            dataSegmentLength,
            target_amount_range1, target_amount_range2,
            &result_count
        );
        clFinish(queue_list[0]);
        printf("result_count=%d \n", result_count);

        char result_file[MAX_LENGTH];
        memset(result_file, '\0', MAX_LENGTH);
        sprintf(result_file, "%s/data/opencode_amount_result_%s.csv",  current_path, expectId);
#ifdef DEBUG
        printf("opencode amount result file: %s\n", result_file);
#endif
        FILE* fp = fopen(result_file, "r");
        if (fp) {
            // file exists
            remove(result_file);
            fclose(fp);
        } else {
            // file doesn't exist
        }

        if(result_count > 0)
        {
            printf("filter opencode when win/loss amount in range ... 1/2\n");
            cl_uint* amountRangeResult1 = (cl_uint*)malloc(sizeof(cl_uint) * result_count);
            run_kernel_find_best_amount(
                context,
                queue_list[0],
                kFindBestAmount,
                opencode_answer_table_result1,
                dataSegmentLength,
                result_count,
                target_amount_range1, target_amount_range2,
                &amountRangeResult1);
            clFinish(queue_list[0]);
#ifdef DEBUG
            for(int i=0; i<=result_count-1; i++ )
            {
                int index = amountRangeResult1[i];
                printf("%s, result[%d]=%f \n", opencodeList[index], index, opencode_answer_table_result1[index]);
            }
#endif
            //寫入檔案 1/2
            fp = fopen(result_file, "a");
            for(int i=0; i<=result_count-1; i++ )
            {
                int index = amountRangeResult1[i];
                char tmp[MAX_LENGTH];
                memset(tmp, '\0', MAX_LENGTH);
                sprintf(tmp, "%s,%f\n",  opencodeList[index], opencode_answer_table_result1[index]);
                fputs(tmp, fp);
            }
            fclose(fp);

            if(amountRangeResult1)
                free(amountRangeResult1);
        }

        // 過濾指定金額 2/2
        //====================================================================
        printf("count opencode when win/loss amount in range ... 2/2\n");
        result_count = 0;
        run_kernel_find_best_amount_count(
            context, 
            queue_list[0],
            kFindBestAmountCount,
            opencode_answer_table_result2,
            dataSegmentLength,
            target_amount_range1, target_amount_range2,
            &result_count
        );
        clFinish(queue_list[0]);
        printf("result_count=%d \n", result_count);

        if(result_count > 0)
        {
            printf("filter opencode when win/loss amount in range ... 2/2\n");
            cl_uint* amountRangeResult2 = (cl_uint*)malloc(sizeof(cl_uint) * result_count);
            run_kernel_find_best_amount(
                context,
                queue_list[0],
                kFindBestAmount,
                opencode_answer_table_result2,
                dataSegmentLength,
                result_count,
                target_amount_range1, target_amount_range2,
                &amountRangeResult2);
            clFinish(queue_list[0]);
#ifdef DEBUG
            for(int i=0; i<=result_count-1; i++ )
            {
                int index = amountRangeResult2[i] + dataSegmentLength;
                printf("%s, result[%d]=%f \n", opencodeList[index], index, opencode_answer_table_result2[amountRangeResult2[i]]);
            }
#endif
            //寫入檔案 2/2
            fp = fopen(result_file, "a");
            for(int i=0; i<=result_count-1; i++ )
            {
                int index = amountRangeResult2[i] + dataSegmentLength;
                char tmp[MAX_LENGTH];
                memset(tmp, '\0', MAX_LENGTH);
                sprintf(tmp, "%s,%f\n",  opencodeList[index], opencode_answer_table_result2[index]);
                fputs(tmp, fp);
            }
            fclose(fp);
            if(amountRangeResult2)
                free(amountRangeResult2);
        }
        
        /* 獲取系統當前日期時間 */
        memset(dateTime, 0, sizeof(dateTime));
        GetDateTime(dateTime);
        printf("The Local date and time is %s\n", dateTime);

        printf("======>send: %s\n", result_file);
        send(forClientSockfd, result_file, sizeof(result_file), 0);
    }
    
    if(total_beton_amount_vector)
        free(total_beton_amount_vector);
    if(total_beton_amount_with_odds_vector)
        free(total_beton_amount_with_odds_vector);

    //release opencode_answer_table Buffer
    clReleaseMemObject(opencode_answer_table_buffer); 

    exit(EXIT_SUCCESS);
}