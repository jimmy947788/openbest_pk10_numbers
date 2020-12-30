#include "../header/utility.h"
  
void checkErr(cl_int err, const char* name)
{
    if(err != CL_SUCCESS)
    {
        printf("ERROR: %s ( %d )\n", name, err);
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
        exit(EXIT_FAILURE);
    }

    /* Access device address size */
    clGetDeviceInfo(device, CL_DEVICE_ADDRESS_BITS, sizeof(addr_data), &addr_data, NULL);			

    /* Access device extensions */
    clGetDeviceInfo(device, CL_DEVICE_EXTENSIONS, 4096 * sizeof(char), ext_data, NULL);			
    
    printf("NAME: %s\nADDRESS_WIDTH: %u\nEXTENSIONS: %s\n", name_data, addr_data, ext_data);
}

cl_uint get_platforms(cl_platform_id **platforms)
{
    cl_int total_platforms = 0;
    cl_int errNum;
    char* ext_data;
    size_t ext_size;

    errNum = clGetPlatformIDs(0, NULL, &total_platforms);
    checkErr((errNum != CL_SUCCESS)? errNum : (total_platforms <= 0 ? -1 : CL_SUCCESS), "clGetPlatformIDs for init.");
#ifdef DEBUG
    printf("Get number of Platforms: %d\n", total_platforms);
#endif

    *platforms = (cl_platform_id*) malloc(sizeof(cl_platform_id) * total_platforms);
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
#ifdef DEBUG
        //printf("Platform ID: %d\n", platformId); 
        printf("Platform ID: %d\nsupports extensions: \n %s\n", platformId, ext_data); 
#endif
    }

    if(ext_data)
        free(ext_data);
    return total_platforms;
}

cl_uint create_gpu_device_list(cl_platform_id platform, cl_device_id** device_list)
{
    cl_uint total_devices = 0;
    cl_int errNum;

    errNum = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 0, NULL, &total_devices);
    if (errNum != CL_SUCCESS && errNum != CL_DEVICE_NOT_FOUND)
    {
        checkErr(errNum, "clGetDeviceIDs");
    } 
    else if (total_devices > 0)
    {
        *device_list = (cl_device_id**)malloc(sizeof(cl_device_id) * total_devices);
        errNum = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, total_devices, *device_list, NULL);
        checkErr(errNum, "clGetDeviceIDs");
        printf("found number of GPU : %d\n", total_devices);
    }
    else
    {
        printf("No CPU devices found.\n");
        exit(EXIT_FAILURE);
    }
    return total_devices;
}

void create_queue_list(cl_context context, 
    cl_device_id* device_list, cl_int total_devices,
    cl_command_queue** queue_list)
{
    cl_int errNum;
    *queue_list = (cl_command_queue*)malloc(sizeof(cl_command_queue) * total_devices);
    for(cl_int i=0; i<=total_devices -1; i++ )
    {
        *(*queue_list + i) = clCreateCommandQueue(context, device_list[i], CL_QUEUE_PROFILING_ENABLE, &errNum);
        checkErr(errNum, "clCreateCommandQueue");
        if(errNum < 0) {
            perror("Couldn't read the buffer");
            exit(EXIT_FAILURE);   
        }
    }
}

void build_program_for_all_devices(
    char* path, 
    cl_context context,
    cl_device_id* device_list,
    cl_program** program)
{
    cl_int errNum;
    char* kernel_program_fullpath = (char*)malloc(sizeof(char) * (strlen(gWorkerFolder) + strlen(path) + 2));
    pathCombine(kernel_program_fullpath, gWorkerFolder, path);
    log_debug("kernel_program_fullpath =%s", kernel_program_fullpath);

    if(!exists(kernel_program_fullpath))
    {
        log_error("Can't find kernel program file...(%s)", kernel_program_fullpath);
        exit(EXIT_FAILURE);
    }

    // Load the kernel source code into the array source_str
    char* programContent = (char*)malloc(MAX_SOURCE_SIZE);
    size_t programSize = readContent(programContent, kernel_program_fullpath);

    // Create a program from the kernel source
    *program = clCreateProgramWithSource(context, 1, 
            (const char **)&programContent, (const size_t *)&programSize, &errNum);
    //checkErr(errNum, "clCreateProgramWithSource");
    //printf("create OpenCL program from %s ........... successful!!\n", kernel_program_path);
    if(programContent)
        free(programContent);
    if(kernel_program_fullpath)
        free(kernel_program_fullpath);

    // Build the program
    //errNum = clBuildProgram(*program, num_devices, device_list, NULL, NULL, NULL);
    errNum = clBuildProgram(*program, 0, NULL, NULL, NULL, NULL);
    //checkErr(errNum, "clBuildProgram");
    // 產出Build cl檔案的log不然cl程式碼寫錯也編譯不出來
    if(errNum < 0){
        // Shows the log
        char* build_log;
        size_t log_size;
        // First call to know the proper size
        clGetProgramBuildInfo(*program, device_list[0], CL_PROGRAM_BUILD_LOG, 0, NULL, &log_size);
        build_log = malloc(log_size+1);
        // Second call to get the log
        clGetProgramBuildInfo(*program, device_list[0], CL_PROGRAM_BUILD_LOG, log_size, build_log, NULL);
        build_log[log_size] = '\0';
        printf("%s\n", build_log);
        if(build_log)
            free(build_log);
        
        exit(EXIT_FAILURE);
    }
}

void executionTime(cl_event event, double* elapsedTime)
{
    cl_ulong start, end;
    double total_time = 0;
    
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_END, sizeof(cl_ulong), &end, NULL);
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_START, sizeof(cl_ulong), &start, NULL);
    total_time = end - start;

    *elapsedTime = (end-start)*1.0e-6f;
    //return (double)(end - start)*(double)(1e-06); // convert nanoseconds to seconds on return
}

int run_kernel_sum_beton_total_amount(
        cl_context context, 
        cl_command_queue queue, 
        cl_kernel kernel,
        int wgaer_length, 
        cl_ushort* one_mask, 
        cl_float* bet_amount, 
        cl_float** result)
{
    cl_int errNum;
    
    printf("clCreateBuffer mask_buffer\n");
    /* Create a write-only buffer to hold the output data */
    cl_mem mask_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_ushort) * gBetonLenght, 
        one_mask, 
        &errNum); 
    if(errNum < 0) {
      perror("Couldn't create a mask_buffer");
      exit(EXIT_FAILURE);
    };

    printf("clCreateBuffer bet_amount_buffer\n");
    cl_mem bet_amount_buffer = clCreateBuffer(context, 
        CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
        sizeof(cl_float) * gBetonLenght * wgaer_length, 
        bet_amount, 
        &errNum);    
    if(errNum < 0) {
      perror("Couldn't create a bet_amount_buffer");
      exit(EXIT_FAILURE);
    };

    cl_mem result_buffer = clCreateBuffer(context,
        CL_MEM_WRITE_ONLY,
        sizeof(cl_float) * gBetonLenght, 
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
    const size_t global_size[] = { gBetonLenght };
    const size_t local_size[] = { 1 };
    errNum = clEnqueueNDRangeKernel(queue, kernel, dim, global_offset, global_size, local_size, 0, NULL,  NULL);

    checkErr(errNum, "clEnqueueNDRangeKernel");    
    printf("pass kernel code to GPU\n");

     /* Read and print the result */
    errNum = clEnqueueReadBuffer(queue, result_buffer, CL_TRUE, 0, sizeof(cl_float) * gBetonLenght, *result, 0, NULL, NULL);
    if(errNum < 0) {
        perror("Couldn't read the buffer");
        exit(EXIT_FAILURE);
    }

    clReleaseMemObject(result_buffer);
    clReleaseMemObject(mask_buffer);
    clReleaseMemObject(bet_amount_buffer);
   
    return 0;
}