
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <sys/types.h>

#include "../header/loadData.h"
#include "../header/config.h"
#include "../header/argument.h"
#include "../header/utility.h"
#include "../header/dateTime.h"
#include "../header/network.h"


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

    laod_args(argc, argv, &kernel_program_file, &log_dir);
    
    if(strlen(kernel_program_file) == 0)
    {
        printf("must be support argument...\n");
        printf("\t--kernel-program <path>\n");
        printf("show help\n");
        printf("\tcalc_opencode_amount -h\n");
        exit(EXIT_SUCCESS);
    }
    
    getcwd(current_path, MAX_LENGTH );
#ifdef DEBUG
    printf("kernel_program_file:%s\n", kernel_program_file);
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

    int beton_count = PK10_BETON_COUNT;
    int wager_length = 0; 
    char expectId[MAX_LENGTH];
    cl_ushort* one_mask = NULL;
    cl_float* beton_amount_table = NULL;
    cl_float* beton_amount_with_odds_table = NULL;
    cl_float* total_beton_amount_vector = NULL;
    cl_float* total_beton_amount_with_odds_vector = NULL;

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
    
    cl_kernel kCalcNumbersRisk[USE_GPU_NUM];
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        kCalcNumbersRisk[num] = clCreateKernel(program, "calc_numbers_risk", &errNum);
        checkErr(errNum, "clCreateKernel");
        printf("Create OpenCL Kernel program :%s[%d]\n", "calc_numbers_risk", num);
    }

    // release OpenCL program
    printf("release OpenCL program");
    clReleaseProgram(program);
    printf(".......... successful!!\n");
    //============================================================================
   
    // load opencode answer table
    //===================================================================================================
    cl_short* opencode_answer_table[USE_GPU_NUM];
    cl_float* opencode_answer_table_result[USE_GPU_NUM];
    char** opencodeList[USE_GPU_NUM];

    char opencode_answer_table_path[MAX_LENGTH];
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        printf("load opencode answer table from csv...%d/%d\n", (num+1), USE_GPU_NUM);
        //fflush(stdout); //不給\n就不給輸出,flush強制輸出
        opencode_answer_table[num] = (cl_short *)malloc(sizeof(cl_short) * PK10_BETON_COUNT * GPU_HANDEL_COUNT[num]);
        opencodeList[num] = (char**)malloc(sizeof(*opencodeList[num]) * GPU_HANDEL_COUNT[num]);
        sprintf(opencode_answer_table_path, "%s/%s", current_path, OPENCODE_ANSWER_TABLE_PATH[num]);
        int ret = load_opnecode_answer_table(opencode_answer_table_path, &opencodeList[num], &opencode_answer_table[num]);
        printf("opencodeList[%d] length:%ld\n", num, ret);
    }


    one_mask = (cl_ushort*)malloc(sizeof(cl_ushort) * PK10_BETON_COUNT);
    for(int i=0; i<=PK10_BETON_COUNT-1; i++ )
    {
        one_mask[i] = 1;
    }
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        printf("alloc opencode_answer_table_result[%d] array (length: %d)\n", num, GPU_HANDEL_COUNT[num]);
        opencode_answer_table_result[num] = (cl_float*)malloc(sizeof(cl_float) * GPU_HANDEL_COUNT[num]);
    }
    
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
    
    //opencl buffer
    cl_mem total_beton_amount_buffer[USE_GPU_NUM];
    cl_mem total_beton_amount_with_odds_buffer[USE_GPU_NUM];
    cl_mem opencode_answer_table_buffer[USE_GPU_NUM];
    cl_mem result_buffer[USE_GPU_NUM];
    cl_buffer_region region;
    //opencl events
    cl_event kernel_events[USE_GPU_NUM];
    cl_event read_events[USE_GPU_NUM];

    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        //create opencode_answer_table Buffer
        opencode_answer_table_buffer[num] = clCreateBuffer(
            context, 
            CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
            sizeof(cl_short) * PK10_BETON_COUNT * GPU_HANDEL_COUNT[num], 
            opencode_answer_table[num], 
            &errNum);    
        if(errNum < 0) {
            perror("Couldn't create a opencode_answer_table_buffer[]");
            exit(EXIT_FAILURE);
        };
    }
    
    //while 重複直行
    //===================================================================================================
    while(true)
    {
        printf("ready to recv data...\n");
        forClientSockfd = accept(sockfd,(struct sockaddr*) &clientInfo, &addrlen);
        memset(recv_buffer, '\0', MAX_BUFFER_SIZE);
        recv(forClientSockfd, recv_buffer, sizeof(recv_buffer), 0);
        printf("======> %s\n", recv_buffer);
        parser_data(recv_buffer, 
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
        beton_amount_table = (cl_float*)malloc(sizeof(cl_float) * PK10_BETON_COUNT * wager_length);
        load_beton_amount_table(beton_amount_table_file, &beton_amount_table);
        total_beton_amount_vector = (cl_float*)malloc(sizeof(cl_float) * PK10_BETON_COUNT);
        run_kernel_sum_beton_total_amount(
            context, 
            queue_list[0], 
            kSumBetonTotalAmount, 
            wager_length,
            one_mask, beton_amount_table,
            &total_beton_amount_vector);
        if(beton_amount_table)
            free(beton_amount_table);
#ifdef DEBUG
        sum = 0;
        for(int i=0; i<=PK10_BETON_COUNT-1; i++)
        {
            sum += total_beton_amount_vector[i];
        }
        printf("====> sum total_beton_amount = %f\n", sum);
#endif

        beton_amount_with_odds_table = (cl_float*)malloc(sizeof(cl_float) * PK10_BETON_COUNT * wager_length);
        load_beton_amount_table(beton_amount_table_with_odds_file, &beton_amount_with_odds_table);
        total_beton_amount_with_odds_vector = (cl_float*)malloc(sizeof(cl_float) * PK10_BETON_COUNT);
        run_kernel_sum_beton_total_amount(
            context, 
            queue_list[0], 
            kSumBetonTotalAmount, 
            wager_length,
            one_mask, beton_amount_with_odds_table, 
            &total_beton_amount_with_odds_vector);
        if(beton_amount_with_odds_table)
            free(beton_amount_with_odds_table);
#ifdef DEBUG
        sum = 0;
        for(int i=0; i<=PK10_BETON_COUNT-1; i++)
        {
            sum += total_beton_amount_with_odds_vector[i];
        }
        printf("====> sum total beton amount with odds = %f\n", sum);
#endif

        clock_t timeStart, timeEnd;
        //計算獎號開出金額 (建立buffer & 設定參數)
        //===================================================================
        timeStart = clock();
        for(int num=0; num<=USE_GPU_NUM-1; num++)
        {
            printf("calc total win/loss amount in opencode list ... %d/%d\n", (num+1), USE_GPU_NUM);
            memset(opencode_answer_table_result[num], 0.0f, GPU_HANDEL_COUNT[num]);
            // creater buffer total_beton_amount_buffer
            total_beton_amount_buffer[num] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR,  sizeof(cl_float) * PK10_BETON_COUNT, total_beton_amount_vector, &errNum); 
            if(errNum < 0) {
                perror("Couldn't create a total_beton_amount_buffer");
                exit(EXIT_FAILURE);
            };
            //create buffer total_beton_amount_with_odds_buffer 
            total_beton_amount_with_odds_buffer[num] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, sizeof(cl_float) * PK10_BETON_COUNT, total_beton_amount_with_odds_vector, &errNum);    
            if(errNum < 0) {
                perror("Couldn't create a total_beton_amount_with_odds_buffer");
                exit(EXIT_FAILURE);
            };

            //create buffer result_buffer
            result_buffer[num] = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(cl_float) * GPU_HANDEL_COUNT[num] ,  NULL,  &errNum);
            if(errNum < 0) {
                perror("Couldn't create a result_buffer");
                exit(EXIT_FAILURE);
            };

            /* Create kernel argument */
            errNum = clSetKernelArg(kCalcNumbersRisk[num], 0, sizeof(cl_mem), &total_beton_amount_buffer[num]);
            if(errNum < 0) {
                perror("Couldn't set a kernel argument (total_beton_amount_buffer)");
                exit(EXIT_FAILURE);
            };

            errNum = clSetKernelArg(kCalcNumbersRisk[num], 1, sizeof(cl_mem), &total_beton_amount_with_odds_buffer[num]);
            if(errNum < 0) {
                perror("Couldn't set a kernel argument (total_beton_amount_with_odds_buffer)");
                exit(EXIT_FAILURE);
            };

            errNum = clSetKernelArg(kCalcNumbersRisk[num], 2, sizeof(cl_mem), &opencode_answer_table_buffer[num]);
            if(errNum < 0) {
                perror("Couldn't set a kernel argument (opencode_answer_table_buffer[0])");
                exit(EXIT_FAILURE);
            };

            errNum = clSetKernelArg(kCalcNumbersRisk[num], 3, sizeof(cl_mem), &result_buffer[num]);
            if(errNum < 0) {
                perror("Couldn't set a kernel argument (result_buffer)");
                exit(EXIT_FAILURE);
            };

            errNum = clSetKernelArg(kCalcNumbersRisk[num], 4, sizeof(cl_int), &beton_count);
            if(errNum < 0) {
                perror("Couldn't set a kernel argument (PK10_BETON_COUNT)");
                exit(EXIT_FAILURE);
            };
        }
        timeEnd = clock();
        printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", "clSetKernelArg", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);

        //計算獎號開出金額 (enqueue task)
        //===================================================================
        timeStart = clock();
        for(int num=0; num<=USE_GPU_NUM-1; num++)
        {
            int dim = 1;
            const size_t global_offset[] = { 0 };
            const size_t global_size[] = { GPU_HANDEL_COUNT[num] };
            const size_t local_size[] = { 1 };
            errNum = clEnqueueNDRangeKernel(queue_list[num], kCalcNumbersRisk[num], dim, global_offset, global_size, local_size, 0, NULL, &kernel_events[num]);
            if(errNum < 0) {
                perror("Couldn't enqueue kernel");
                exit(EXIT_FAILURE);
            }
        }
        clWaitForEvents(2, kernel_events);
        timeEnd = clock();
        printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", "clEnqueueNDRangeKernel", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
        
        //計算獎號開出金額 (reqd result from buffer)
        //===================================================================
        timeStart = clock();
        for(int num=0; num<=USE_GPU_NUM-1; num++)
        {
            errNum = clEnqueueReadBuffer(queue_list[num], result_buffer[num], CL_FALSE, 0, sizeof(cl_float) * GPU_HANDEL_COUNT[num], opencode_answer_table_result[num], 0, NULL, &read_events[num]);
            if(errNum < 0) {
                perror("Couldn't read the buffer");
                exit(EXIT_FAILURE);
            }
        }
        clWaitForEvents(2, read_events);
        timeEnd = clock();
        printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", "clEnqueueReadBuffer", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);


#ifdef DEBUG
        double dddd = 0;
        executionTime(kernel_events[0], &dddd);
        printf("kernel_events[0] time is %0.3f\n", dddd);
        executionTime(kernel_events[1], &dddd);
        printf("kernel_events[1] time is %0.3f\n", dddd);
        executionTime(read_events[0], &dddd);
        printf("read_events[0] time is %0.3f\n", dddd);
        executionTime(read_events[1], &dddd);
        printf("read_events[1] time is %0.3f\n", dddd);
#endif
        for(int num=0; num<=USE_GPU_NUM-1; num++)
        {
            printf("release total_beton_amount_buffer[%d]\n", num);
            clReleaseMemObject(total_beton_amount_buffer[num]);
            printf("release total_beton_amount_with_odds_buffer[%d]\n", num);
            clReleaseMemObject(total_beton_amount_with_odds_buffer[num]);
        }
        
        printf("release kernel_events\n");
        for(int num=0; num<=USE_GPU_NUM-1; num++)
            clReleaseEvent(kernel_events[num]);
        
        printf("release read_events\n");
        for(int num=0; num<=USE_GPU_NUM-1; num++)
            clReleaseEvent(read_events[num]);
        
        printf("release result_buffer\n");
        for(int num=0; num<=USE_GPU_NUM-1; num++)
            clReleaseEvent(result_buffer[num]);

#ifdef DEBUG
        for(int i=0; i<=20 - 1; i++)
        {
            printf("%s, result[%d]=%0.6f \n", opencodeList[0][i], i, opencode_answer_table_result[0][i]);
        }

        for(int i= GPU_HANDEL_COUNT[0] - 1; i>=GPU_HANDEL_COUNT[0] -20; i--)
        {
            printf("%s, result[%d]=%0.6f \n", opencodeList[0][i], i, opencode_answer_table_result[0][i]);
        }
        for(int i=0; i<=20 - 1; i++)
        {
            printf("%s, result[%d]=%0.6f \n",opencodeList[1][i], i, opencode_answer_table_result[1][i]);
        }
        for(int i=GPU_HANDEL_COUNT[1]-1; i>=GPU_HANDEL_COUNT[1] -20; i--)
        {
            printf("%s, result[%d]=%0.6f \n", opencodeList[1][i], i, opencode_answer_table_result[1][i]);
        }
#endif        
        //clock_t timeStart, timeEnd;
        timeStart = clock();
        char result_file[MAX_LENGTH];
        memset(result_file, '\0', MAX_LENGTH);
        sprintf(result_file, "%s/data/opencode_amount_result_%s.csv", current_path, expectId);
        //check result file exist
        FILE* fp = fopen(result_file, "r");
        if (fp) {
            // file exists
            remove(result_file);
            fclose(fp);
        }
        
        char tmp[MAX_LENGTH];
        //寫入檔案 1/2
        fp = fopen(result_file, "a");
        
        for(int num=0; num<=USE_GPU_NUM - 1; num++)
        {
            for(int i=0; i<= GPU_HANDEL_COUNT[num] - 1; i++ )
            {
                float amount = opencode_answer_table_result[num][i];
                if(target_amount_range1 <=amount && amount <= target_amount_range2)
                {
                    memset(tmp, '\0', MAX_LENGTH);
                    sprintf(tmp, "%s,%0.6f\n", opencodeList[num][i], amount);
                    fputs(tmp, fp);
                }
            }
        }
        fclose(fp);
        timeEnd = clock();
        printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", "save result to csv", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
     
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