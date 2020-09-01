
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
#include "../header/logger.h"

int main(int argc, char* argv[])
{
    cl_int errNum;    
    char kernel_program_file[MAX_LENGTH] = "";
    char opencode_answer_table_file[MAX_LENGTH] = "";
    char beton_amount_table_file[MAX_LENGTH] = "";
    char beton_amount_table_with_odds_file[MAX_LENGTH] = "";
    char work_folder[MAX_LENGTH] = "";
    char log_dir[MAX_LENGTH];
    strcpy(log_dir, "log/");
    char temp_path[MAX_LENGTH] = "";

    laod_args(argc, argv, &kernel_program_file, &work_folder, &log_dir);
    
    if(strlen(kernel_program_file) == 0 || strlen(work_folder) == 0)
    {
        printf("must be support argument...");
        printf("\t--kernel-program <path>");
        printf("\t--work-folder  <path>");
        printf("show help");
        printf("\tcalc_opencode_amount -h");
        exit(EXIT_SUCCESS);
    }
    
    char log_file[MAX_LENGTH];
    sprintf(log_file, "%s/%scalc_opencode_amount.log", work_folder, log_dir);
    FILE *logfp = fopen(log_file, "a+");
    log_add_fp(logfp, LOG_TRACE);

#ifdef DEBUG
    log_debug("kernel_program_file: %s", kernel_program_file);
    log_debug("log_file: %s", log_file);
    log_debug("work folder: %s", work_folder);
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

    log_info("get OpenCL platforms");
    total_platforms = get_platforms(&platforms);
    log_info(" ........... successful!!(total_platforms=%d)", total_platforms);

    log_info("create OpenCL GPU devices");
    total_devices = create_gpu_device_list(platforms[0], &device_list);
    log_info(" ........... successful!!(total_devices=%d)", total_devices);

    // Create an OpenCL context
    log_info("create OpenCL context for all GPU");
    context = clCreateContext(NULL, total_devices, device_list, &contextCallback, NULL, &errNum);
    checkErr(errNum, "clCreateContext");
    log_info(" ........... successful!!");

    log_info("create OpenCL command queue for all devics");
    create_queue_list(context, device_list, total_devices, &queue_list);
    log_info(" ........... successful!!(total command queue=%d)", total_devices);

    log_info("build OpenCL program from");
    memset(temp_path, '\0', MAX_LENGTH);
    sprintf(temp_path, "%s%s", work_folder, kernel_program_file);
    //log_info("full kernel_program_file:%s", temp_path);
    // build an OpenCL program
    build_program_for_all_devices(temp_path, context, device_list, &program);
    log_info(".......... successful!!");

    // Create OpenCL Kernel function
    cl_kernel kSumBetonTotalAmount = clCreateKernel(program, "sum_beton_total_amount", &errNum);
    checkErr(errNum, "clCreateKernel");
    log_info("Create OpenCL Kernel program :%s", "sum_beton_total_amount");
    
    cl_kernel kCalcNumbersRisk[USE_GPU_NUM];
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        kCalcNumbersRisk[num] = clCreateKernel(program, "calc_numbers_risk", &errNum);
        checkErr(errNum, "clCreateKernel");
        log_info("Create OpenCL Kernel program :%s[%d]", "calc_numbers_risk", num);
    }

    // release OpenCL program
    log_info("release OpenCL program");
    clReleaseProgram(program);
    log_info(".......... successful!!");
    //============================================================================
   
    // load opencode answer table
    //===================================================================================================
    cl_short* opencode_answer_table[USE_GPU_NUM];
    cl_float* opencode_answer_table_result[USE_GPU_NUM];
    char** opencodeList[USE_GPU_NUM];
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        log_info("load opencode answer table from %s...%d/%d", OPENCODE_ANSWER_TABLE_PATH[num], (num+1), USE_GPU_NUM);
        //fflush(stdout); //不給就不給輸出,flush強制輸出
        opencode_answer_table[num] = (cl_short *)malloc(sizeof(cl_short) * PK10_BETON_COUNT * GPU_HANDEL_COUNT[num]);
        opencodeList[num] = (char**)malloc(sizeof(*opencodeList[num]) * GPU_HANDEL_COUNT[num]);
        memset(temp_path, '\0', MAX_LENGTH);
        sprintf(temp_path, "%s%s", work_folder, OPENCODE_ANSWER_TABLE_PATH[num]);
        int ret = load_opnecode_answer_table(temp_path, &opencodeList[num], &opencode_answer_table[num]);
        log_info("opencodeList[%d] length:%ld", num, ret);
    }

    one_mask = (cl_ushort*)malloc(sizeof(cl_ushort) * PK10_BETON_COUNT);
    for(int i=0; i<=PK10_BETON_COUNT-1; i++ )
    {
        one_mask[i] = 1;
    }
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        log_info("alloc opencode_answer_table_result[%d] array (length: %d)", num, GPU_HANDEL_COUNT[num]);
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
    //float target_amount_range1 = 0;
    //float target_amount_range2 = 0;
    float target_amount = 0;
    float tolerance = 0;
    int  result_count = 0;
    
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
        log_info("ready to recv data...");
        forClientSockfd = accept(sockfd,(struct sockaddr*) &clientInfo, &addrlen);
        memset(recv_buffer, '\0', MAX_BUFFER_SIZE);
        recv(forClientSockfd, recv_buffer, sizeof(recv_buffer), 0);
        log_info("======> %s", recv_buffer);
        parser_data(recv_buffer, 
            beton_amount_table_file, 
            beton_amount_table_with_odds_file, 
            &wager_length, 
            expectId,
            &target_amount,
            &tolerance,
            &result_count);
        log_info("beton_amount_table_file = %s", beton_amount_table_file);
        log_info("beton_amount_table_with_odds_file = %s", beton_amount_table_with_odds_file);
        log_info("wager_length = %d", wager_length);
        log_info("expectId = %s", expectId);
        log_info("target_amount = %f", target_amount);
        log_info("tolerance = %f", tolerance);
        log_info("result_count = %d", result_count);
        
        //target_amount_range1 = target_amount - (target_amount * tolerance);
        //target_amount_range2 = target_amount + (target_amount * tolerance);
        //log_info("target_amount_range1 = %f, target_amount_range2= %f ", target_amount_range1, target_amount_range2);
        if(tolerance ==1 )
            log_info("user winner target_amount=%f", target_amount);
        else //if(tolerance ==-1)
            log_info("banker winner target_amount=%f", target_amount);

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
        log_debug("====> sum total_beton_amount = %f", sum);
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
        log_debug("====> sum total beton amount with odds = %f", sum);
#endif

        clock_t timeStart, timeEnd;
        //計算獎號開出金額 (建立buffer & 設定參數)
        //===================================================================
        timeStart = clock();
        for(int num=0; num<=USE_GPU_NUM-1; num++)
        {
            log_info("calc total win/loss amount in opencode list ... %d/%d", (num+1), USE_GPU_NUM);
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
        log_info("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms", "clSetKernelArg", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);

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
        log_info("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms", "clEnqueueNDRangeKernel", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
        
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
        log_info("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms", "clEnqueueReadBuffer", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);


#ifdef DEBUG
        double dddd = 0;
        executionTime(kernel_events[0], &dddd);
        log_debug("kernel_events[0] time is %0.3f", dddd);
        executionTime(kernel_events[1], &dddd);
        log_debug("kernel_events[1] time is %0.3f", dddd);
        executionTime(read_events[0], &dddd);
        log_debug("read_events[0] time is %0.3f", dddd);
        executionTime(read_events[1], &dddd);
        log_debug("read_events[1] time is %0.3f", dddd);
#endif
        for(int num=0; num<=USE_GPU_NUM-1; num++)
        {
            log_info("release total_beton_amount_buffer[%d]", num);
            clReleaseMemObject(total_beton_amount_buffer[num]);
            log_info("release total_beton_amount_with_odds_buffer[%d]", num);
            clReleaseMemObject(total_beton_amount_with_odds_buffer[num]);
        }
        
        log_info("release kernel_events");
        for(int num=0; num<=USE_GPU_NUM-1; num++)
            clReleaseEvent(kernel_events[num]);
        
        log_info("release read_events");
        for(int num=0; num<=USE_GPU_NUM-1; num++)
            clReleaseEvent(read_events[num]);
        
        log_info("release result_buffer");
        for(int num=0; num<=USE_GPU_NUM-1; num++)
            clReleaseEvent(result_buffer[num]);

#ifdef DEBUG
        for(int i=0; i<=20 - 1; i++)
        {
            log_debug("%s, result[%d]=%0.6f ", opencodeList[0][i], i, opencode_answer_table_result[0][i]);
        }

        for(int i= GPU_HANDEL_COUNT[0] - 1; i>=GPU_HANDEL_COUNT[0] -20; i--)
        {
            log_debug("%s, result[%d]=%0.6f ", opencodeList[0][i], i, opencode_answer_table_result[0][i]);
        }
        for(int i=0; i<=20 - 1; i++)
        {
            log_debug("%s, result[%d]=%0.6f ",opencodeList[1][i], i, opencode_answer_table_result[1][i]);
        }
        for(int i=GPU_HANDEL_COUNT[1]-1; i>=GPU_HANDEL_COUNT[1] -20; i--)
        {
            log_debug("%s, result[%d]=%0.6f ", opencodeList[1][i], i, opencode_answer_table_result[1][i]);
        }
#endif        
        //clock_t timeStart, timeEnd;
        timeStart = clock();
        char result_file[MAX_LENGTH];
        memset(result_file, '\0', MAX_LENGTH);
        sprintf(result_file, "%s/data/opencode_amount_result_%s.csv", work_folder, expectId);
        //check result file exist
        FILE* fp = fopen(result_file, "r");
        if (fp) {
            // file exists
            remove(result_file);
            fclose(fp);
        }

        int target_amount_counter = 0;
        char tmp[MAX_LENGTH];
        //將到達條件金額寫入檔案 
        fp = fopen(result_file, "a");
        for(int num=0; num<=USE_GPU_NUM - 1; num++)
        {
            for(int i=0; i<= GPU_HANDEL_COUNT[num] - 1; i++ )
            {
                float amount = opencode_answer_table_result[num][i];
                if(tolerance == 1)
                {
                    if(target_amount <= amount ) //玩家贏錢
                    {
                        memset(tmp, '\0', MAX_LENGTH);
                        sprintf(tmp, "%s,%0.6f\n", opencodeList[num][i], amount);
                        fputs(tmp, fp);
                        target_amount_counter++;
                    }
                }
                else
                {
                    if(amount <= target_amount) //莊家贏錢
                    {
                        memset(tmp, '\0', MAX_LENGTH);
                        sprintf(tmp, "%s,%0.6f\n", opencodeList[num][i], amount);
                        fputs(tmp, fp);
                        target_amount_counter++;
                    }
                }
            }
        }
        fclose(fp);
        timeEnd = clock();
        log_info("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms", "save result to csv", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);

        //讀取所有符合開獎結果CSV
        log_info("read data from csv file");
        int target_amount_result_index = 0;
        char** target_amount_results;
        target_amount_results = (char**)malloc(sizeof(*target_amount_results) * target_amount_counter);
        fp = fopen(result_file, "r");
        while( fgets(tmp, MAX_LENGTH, fp) ) {
            //log_info("%s",line);
            *(target_amount_results + target_amount_result_index) = (char*) malloc(sizeof(char) * MAX_LENGTH);
            memset(*(target_amount_results + target_amount_result_index), '\0', MAX_LENGTH);
            strcpy(*(target_amount_results + target_amount_result_index), tmp);
            target_amount_result_index++;
        }
        log_info("target_amount_counter = %d", target_amount_counter );

        //亂數讀取 result_count 筆所有符合開獎結果
        //temp_target_amount_results : 把所有結果組成很長的字串透過socket回傳
        //target_amount_results[rand_num] : 1-3-7-2-9-4-10-8-5-6,0.000000\n
        //target_amount_results[rand_num] : {獎號},{金額}\n
        int rand_num = 0;
        time_t t;
        char temp_target_amount_results[MAX_SOURCE_SIZE];
        memset(temp_target_amount_results, '\0', MAX_SOURCE_SIZE);
        log_info("randam %d data to temp_target_amount_results array.", result_count);
        if( target_amount_counter > 0)
        {
            srand((unsigned) time(&t));
            for( int i = 0 ; i <= result_count-1 ; i++ ) {
                rand_num = rand() % target_amount_counter;
#ifdef DEBUG
                log_debug("rand_num[%d] = %d", i, rand_num);
                log_debug("target_amount_results[%d] = %s", rand_num, target_amount_results[rand_num]);
#endif
                strcat (temp_target_amount_results, target_amount_results[rand_num]);
                //log_debug("temp_target_amount_results = %s", temp_target_amount_results); 
            }
        }
        log_info("free every target_amount_results array.");
        for(int i=0; i<=target_amount_result_index-1; i++)
        {
            if(*(target_amount_results + i))
                free(*(target_amount_results + i));
        }
        if(target_amount_results)
            free(target_amount_results);

        /* 獲取系統當前日期時間 */
        memset(dateTime, 0, sizeof(dateTime));
        GetDateTime(dateTime);
        log_info("The Local date and time is %s", dateTime);

        send(forClientSockfd, temp_target_amount_results, sizeof(temp_target_amount_results), 0);
    }
    
    if(total_beton_amount_vector)
        free(total_beton_amount_vector);
    if(total_beton_amount_with_odds_vector)
        free(total_beton_amount_with_odds_vector);

    //release opencode_answer_table Buffer
    clReleaseMemObject(opencode_answer_table_buffer); 

    fclose(logfp);
    exit(EXIT_SUCCESS);
}