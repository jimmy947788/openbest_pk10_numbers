
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <sys/types.h>

#include "../header/common.h"
#include "../header/loadData.h"
#include "../header/config.h"
#include "../header/argument.h"
#include "../header/utility.h"
#include "../header/dateTime.h"
#include "../header/network.h"
#include "../header/logger.h"
#include "../header/mystring.h"

extern char     gWorkerFolder[MAX_LENGTH];
extern char**   gBetonList;
extern uint32      gBetonLenght;

extern char**   gOpencodeList;
extern uint32      gOpencodeLenght;

extern uint32   GPU_HANDEL_COUNT[USE_GPU_NUM];


void init_log(FILE **logfp, const char* log_dir)
{
    char log_file[MAX_LENGTH];
    sprintf(log_file, "%s/%scalc_opencode_amount.log", gWorkerFolder, log_dir);
    *logfp = fopen(log_file, "a+");
    log_add_fp(*logfp, LOG_TRACE);
}

int main(int argc, char* argv[])
{
    cl_int errNum;    
    char kernel_program_file[MAX_LENGTH] = "";
    char beton_amount_table_file[MAX_LENGTH] = "";
    char beton_amount_table_with_odds_file[MAX_LENGTH] = "";
    FILE *logfp;
    char log_dir[MAX_LENGTH];
    clock_t timeStart, timeEnd;

    laod_args(argc, argv, &kernel_program_file, &gWorkerFolder, &log_dir);
    
    printf("log_dir=%s", log_dir);
    strcpy(log_dir, "log/");

    if(strlen(kernel_program_file) == 0 || strlen(gWorkerFolder) == 0)
    {
        printf("must be support argument...");
        printf("\t--kernel-program <path>");
        printf("\t--worker-folder  <path>");
        printf("show help");
        printf("\tcalc_opencode_amount -h");
        exit(EXIT_SUCCESS);
    }
    log_debug("kernel_program_file: %s", kernel_program_file);
    //log_debug("log_file: %s", log_file);
    log_debug("worker folder: %s", gWorkerFolder);

    init_log(&logfp, log_dir);
    loadBetonList();
    loadOpencodeList();
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        GPU_HANDEL_COUNT[num] = gOpencodeLenght / USE_GPU_NUM;
        log_info("GPU_HANDEL_COUNT[%d]=%d", num, GPU_HANDEL_COUNT[num]);
    }


#ifdef PK10
    log_info("this program was for PK10 (OPENCODE_COUNT=%d, BETON_COUNT=%d)...", gOpencodeLenght, gBetonLenght);    
#elif defined SSC 
    log_info("this program was for SSC (OPENCODE_COUNT=%d, BETON_COUNT=%d)...", gOpencodeLenght, gBetonLenght);    
#endif

    int total_platforms = 0;
    cl_platform_id* platforms = NULL;
    int total_devices = 0;
    cl_device_id* device_list = NULL;
    cl_context context = NULL;
    cl_program* program = NULL;
    cl_command_queue* queue_list = NULL;

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
    //log_info("full kernel_program_file:%s", temp_path);
    // build an OpenCL program
    build_program_for_all_devices(kernel_program_file, context, device_list, &program);
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
    cl_uchar* opencodeAnswerTableVector[USE_GPU_NUM];
    unsigned long long opencodeAnswerTableVectorLength = gBetonLenght * GPU_HANDEL_COUNT[0];
    char** opencodeList[USE_GPU_NUM];
    
    cl_float* opencodeResultVector[USE_GPU_NUM];
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        log_info("load opencode answer table from %s...%d/%d", OPENCODE_ANSWER_TABLE_PATH[num], (num+1), USE_GPU_NUM);
        //fflush(stdout); //不給就不給輸出,flush強制輸出
        opencodeAnswerTableVector[num] = (cl_uchar*)malloc(sizeof(cl_uchar) * opencodeAnswerTableVectorLength);
        opencodeList[num] = (char**)malloc(sizeof(char*) * GPU_HANDEL_COUNT[num]);
        
        int ret = loadOpencodeAnswerTableVector(
            opencodeAnswerTableVector[num], 
            opencodeList[num],
            OPENCODE_ANSWER_TABLE_PATH[num]);
        log_info("opencodeList[%d] length:%ld", num, ret);
    }

    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        log_info("alloc opencode_answer_table_result[%d] array (length: %d)", num, GPU_HANDEL_COUNT[num]);
        opencodeResultVector[num] = (cl_float*)malloc(sizeof(cl_float) * GPU_HANDEL_COUNT[num]);
    }
 
    
    //openc input & output
    cl_ushort* one_mask = NULL;
    cl_float* betsAmountVector = NULL;
    cl_float* betsAmountWithOddsVector = NULL;
    cl_float* totalBetsAmountVector = NULL;
    cl_float* totalBetsAmountWithOddsVector = NULL;

    //opencl buffer
    cl_mem total_beton_amount_buffer[USE_GPU_NUM];
    cl_mem total_beton_amount_with_odds_buffer[USE_GPU_NUM];
    cl_mem opencode_answer_table_buffer[USE_GPU_NUM];
    cl_mem result_buffer[USE_GPU_NUM];
 
    //opencl events
    cl_event kernel_events[USE_GPU_NUM];
    cl_event read_events[USE_GPU_NUM];

    log_debug("opencodeAnswerTableVector[0][0]=%d", opencodeAnswerTableVector[0][0]);
    log_debug("opencodeAnswerTableVector[0][1]=%d", opencodeAnswerTableVector[0][1]);
    log_debug("opencodeAnswerTableVector[0][5883099999]=%d", opencodeAnswerTableVector[0][5883099999]);
    log_debug("opencodeAnswerTableVector[0][5883100000]=%d", opencodeAnswerTableVector[0][5883100000]);

    log_debug("opencodeAnswerTableVector[1][0]=%d", opencodeAnswerTableVector[1][0]);
    log_debug("opencodeAnswerTableVector[1][1]=%d", opencodeAnswerTableVector[1][1]);
    log_debug("opencodeAnswerTableVector[1][5883099999]=%d", opencodeAnswerTableVector[1][5883099999]);
    log_debug("opencodeAnswerTableVector[1][5883100000]=%d", opencodeAnswerTableVector[1][5883100000]);
    //
    for(int num=0; num<=USE_GPU_NUM-1; num++)
    {
        //create opencode_answer_table Buffer
        opencode_answer_table_buffer[num] = clCreateBuffer(
            context, 
            CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, 
            sizeof(cl_uchar) * opencodeAnswerTableVectorLength, 
            opencodeAnswerTableVector[num], 
            &errNum);    
        if(errNum < 0) {
            perror("Couldn't create a opencode_answer_table_buffer[]");
            exit(EXIT_FAILURE);
        };
    }
    
    //while 重複直行
    //===================================================================================================
    int     forClientSockfd = 0, sockfd = 0;
    struct  sockaddr_in clientInfo;
    int     addrlen = sizeof(clientInfo);
    char    dateTime[_DATETIME_SIZE];
    char*   recvBuffer;
    int     recvBufferSize = MAX_BUFFER_SIZE;
    char*   recvBufferStrip = NULL;
    char**  recvRows = NULL;
    int     recvRowLength = 0;
    char**  recvColumns = NULL;
    int     recvColumnLength = 0;
    char**  rawDatalist = NULL;
    int     rawDatalistLength = 0; 
    int     wagerLength = 0;
    char    expectId[MAX_LENGTH];
    int     direction = 0;
    float   killRate = 0;
    int     resultLength=0;
    float   totalBetsAmount;
    float   targetAmount = 0;
    sockfd = create_socket();

    log_info("init one_mask ...");
    one_mask = (cl_ushort*)malloc(sizeof(cl_ushort) * gBetonLenght);
    for(int i = 0; i< gBetonLenght-1; i++)
    {
        one_mask[i] = 1;
    }

    while(true)
    {
        log_info("ready to recv data...(recv buffer size:%d)", recvBufferSize);
        forClientSockfd = accept(sockfd,(struct sockaddr*) &clientInfo, &addrlen);
        
        recvBuffer = (char*)malloc(sizeof(char) * recvBufferSize+2);
        memset(recvBuffer, '\0', recvBufferSize+2);
        recv(forClientSockfd, recvBuffer, sizeof(char) * recvBufferSize , 0);
        //log_debug("======> %s", recv_buffer);

        if(strstr(recvBuffer, "LEN:") != NULL)
        {
            //取得下一次封包大小
            log_debug("recv raw data: %s", recvBuffer);
            recvBufferStrip = substring(recvBuffer, strlen("LEN:"), strlen(recvBuffer));
            recvBufferSize = strtol(recvBufferStrip, NULL, 10);
            log_info("data length:%d", recvBufferSize);

            send(forClientSockfd, "LEN,OK", sizeof("LEN,OK"), 0);
            log_info("send back LEN process done!");
        }
        else if(strstr(recvBuffer, "DATA:") != NULL)
        {
            log_debug("recv raw data: %s", recvBuffer);
            timeStart = clock();
            recvBufferStrip = substring(recvBuffer, strlen("DATA:"), strlen(recvBuffer) );
            log_debug("recvBufferStrip=%s", recvBufferStrip);
            
            //把資料切分出行
            recvRowLength = count(recvBufferStrip, '^') + 1;
            log_debug("recvRowLength=%d", recvRowLength);
            char** recvRows = (char**)malloc(sizeof(char*) * recvRowLength);
            split(recvRows, recvBufferStrip, "^");

            //第一行是運算參數
            loadParmeters(&wagerLength, &expectId, &direction, &killRate, &resultLength, recvRows[0]);
            log_debug("wager_length=%d, expectId=%s, direction=%d, killRate=%f, resultLength=%d", 
                wagerLength, 
                expectId, 
                direction, 
                killRate,
                resultLength);

            rawDatalist = (recvRows + 1);  //傳入陣列從1開始     
            rawDatalistLength = recvRowLength - 1; //少一筆因為第比是計算參數  
            log_debug("betsAmountVector length is %d", gBetonLenght * wagerLength);
            betsAmountVector = (cl_float*)malloc(sizeof(cl_float)*  gBetonLenght * wagerLength);
            memset(betsAmountVector, 0, gBetonLenght * wagerLength);
            
            betsAmountWithOddsVector = (cl_float*)malloc(sizeof(cl_float) * gBetonLenght * wagerLength);
            memset(betsAmountWithOddsVector, 0, gBetonLenght * wagerLength);

            loadRowData2BetsAmountVector(
                betsAmountVector,
                betsAmountWithOddsVector,
                &totalBetsAmount,
                rawDatalist, 
                rawDatalistLength
            );

            /*
            for(int i=0; i<= gBetonList-1; i++ )
            {
                if(betsAmountVector[i] > 0)
                    log_debug("betsAmountVector[%d]= %f", i, betsAmountVector[i]);
            }*/
            
            timeEnd = clock();
            log_info("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms", "bets_to_onehot", (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
            
            targetAmount = totalBetsAmount * killRate;
            log_info("totalBetsAmount=%0.6f, targetAmount=%0.6f, direction=%d", totalBetsAmount, targetAmount, direction);

            if(direction ==1 )
                log_info("user winner target_amount=%f", targetAmount);
            else //if(tolerance ==-1)
                log_info("banker winner target_amount=%f", targetAmount);


#ifdef DEBUG
            float sum = 0;
#endif
            totalBetsAmountVector = (cl_float*)malloc(sizeof(cl_float) * gBetonLenght);
            run_kernel_sum_beton_total_amount(
                context, 
                queue_list[0], 
                kSumBetonTotalAmount, 
                wagerLength,
                one_mask, 
                betsAmountVector,
                &totalBetsAmountVector);
            if(betsAmountVector)
                free(betsAmountVector);
#ifdef DEBUG
            sum = 0;
            for(int i=0; i<=gBetonLenght-1; i++)
            {
                //printf("%f,", totalBetsAmountVector[i]);
                sum += totalBetsAmountVector[i];
                //if(totalBetsAmountVector[i] > 0)
                //    log_debug("totalBetsAmountVector[%d]= %f", i, totalBetsAmountVector[i]);
            }
            //printf("\n");
            log_debug("====> sum total_beton_amount = %f", sum);
#endif
            totalBetsAmountWithOddsVector = (cl_float*)malloc(sizeof(cl_float) * gBetonLenght);
            run_kernel_sum_beton_total_amount(
                context, 
                queue_list[0], 
                kSumBetonTotalAmount, 
                wagerLength,
                one_mask, 
                betsAmountWithOddsVector, 
                &totalBetsAmountWithOddsVector);
            if(betsAmountWithOddsVector)
                free(betsAmountWithOddsVector);
#ifdef DEBUG
            sum = 0;
            for(int i=0; i<= gBetonLenght-1; i++)
            {
               // printf("%f,", totalBetsAmountWithOddsVector[i]);
                sum += totalBetsAmountWithOddsVector[i];
                //if(totalBetsAmountWithOddsVector[i] > 0)
                //    log_debug("totalBetsAmountWithOddsVector[%d]= %f", i, totalBetsAmountWithOddsVector[i]);
            }
            log_debug("====> sum total beton amount with odds = %f", sum);
            //printf("\n");
#endif
            clock_t timeStart, timeEnd;
            //計算獎號開出金額 (建立buffer & 設定參數)
            //===================================================================
            timeStart = clock();
            for(int num=0; num<=USE_GPU_NUM-1; num++)
            {
                log_info("clSetKernelArg... %d/%d", (num+1), USE_GPU_NUM);
                //memset(opencodeResultVector[num], 0.0f, GPU_HANDEL_COUNT[num]);
                // creater buffer total_beton_amount_buffer
                total_beton_amount_buffer[num] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR,  sizeof(cl_float) * gBetonLenght, totalBetsAmountVector, &errNum); 
                if(errNum < 0) {
                    perror("Couldn't create a total_beton_amount_buffer");
                    exit(EXIT_FAILURE);
                };
                //create buffer total_beton_amount_with_odds_buffer 
                total_beton_amount_with_odds_buffer[num] = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR, sizeof(cl_float) * gBetonLenght, totalBetsAmountWithOddsVector, &errNum);    
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

                errNum = clSetKernelArg(kCalcNumbersRisk[num], 4, sizeof(cl_uint), &gBetonLenght);
                if(errNum < 0) {
                    perror("Couldn't set a kernel argument (beton_count)");
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
                log_info("clEnqueueNDRangeKernel... %d/%d", (num+1), USE_GPU_NUM);
                int dim = 1;
                const size_t global_work_offset[] = { 0 };
                const size_t global_work_size[] = { GPU_HANDEL_COUNT[num] };
                const size_t local_work_size[] = { 1 };
                errNum = clEnqueueNDRangeKernel(
                    queue_list[num], 
                    kCalcNumbersRisk[num], 
                    dim, 
                    global_work_offset, 
                    global_work_size, 
                    local_work_size, 
                    0, 
                    NULL, 
                    &kernel_events[num]);
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
                log_info("clEnqueueReadBuffer... %d/%d", (num+1), USE_GPU_NUM);
                
                errNum = clEnqueueReadBuffer(
                    queue_list[num], 
                    result_buffer[num], 
                    CL_FALSE, 
                    0, 
                    sizeof(cl_float) * GPU_HANDEL_COUNT[num], 
                    opencodeResultVector[num], 
                    0, 
                    NULL, 
                    &read_events[num]);
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
                log_debug("%s, result[%d]=%0.6f ", opencodeList[0][i], i, opencodeResultVector[0][i]);
            }

            for(int i= GPU_HANDEL_COUNT[0] - 1; i>=GPU_HANDEL_COUNT[0] -20; i--)
            {
                log_debug("%s, result[%d]=%0.6f ", opencodeList[0][i], i, opencodeResultVector[0][i]);
            }
            for(int i=0; i<=20 - 1; i++)
            {
                log_debug("%s, result[%d]=%0.6f ",opencodeList[1][i], i, opencodeResultVector[1][i]);
            }
            for(int i=GPU_HANDEL_COUNT[1]-1; i>=GPU_HANDEL_COUNT[1] -20; i--)
            {
                log_debug("%s, result[%d]=%0.6f ", opencodeList[1][i], i, opencodeResultVector[1][i]);
            }
           /*
            for(int i=0; i<= GPU_HANDEL_COUNT[1] - 1; i++)
            {
                //08,08,05,07,09
                if( opencodeResultVector[0][i] != 0)
                {
                    log_debug("%s, result[%d]=%0.6f ", opencodeList[0][i], i, opencodeResultVector[0][i]);
                }
            }
            for(int i=0; i<= GPU_HANDEL_COUNT[1] - 1; i++)
            {
                //08,08,05,07,09
                if( opencodeResultVector[1][i] != 0)
                {
                    log_debug("%s, result[%d]=%0.6f ", opencodeList[1][i], i, opencodeResultVector[1][i]);
                }
            }*/
    #endif

            //clock_t timeStart, timeEnd;
            timeStart = clock();
            char result_file[MAX_LENGTH];
            memset(result_file, '\0', MAX_LENGTH);
            sprintf(result_file, "%s/data/opencode_amount_result_%s.csv", gWorkerFolder, expectId);
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
            cl_float limit_amount = 0;
            for(int num=0; num<=USE_GPU_NUM - 1; num++)
            {
                for(int i=0; i<= GPU_HANDEL_COUNT[num] - 1; i++ )
                {
                    cl_float amount = opencodeResultVector[num][i];
                    if(direction == 1)
                    {
                        if(targetAmount <= amount ) //玩家贏錢
                        {
                            memset(tmp, '\0', MAX_LENGTH);
                            sprintf(tmp, "%s,%0.6f\n", opencodeList[num][i], amount);
                            fputs(tmp, fp);
                            target_amount_counter++;
                        }
                    }
                    else
                    {
                        if(amount <= targetAmount) //莊家贏錢
                        {
                            memset(tmp, '\0', MAX_LENGTH);
                            sprintf(tmp, "%s,%0.6f\n", opencodeList[num][i], amount);
                            fputs(tmp, fp);
                            target_amount_counter++;
                        }
                    }

                    if(amount <= limit_amount)
                    {
                        limit_amount = amount;
                    }
                }
            }

            //找不到目標金額獎號
            if(target_amount_counter == 0)
            {
                for(int num=0; num<=USE_GPU_NUM - 1; num++)
                {
                    for(int i=0; i<= GPU_HANDEL_COUNT[num] - 1; i++ )
                    {
                        cl_float amount = opencodeResultVector[num][i];
                        if(amount == limit_amount) 
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

            // 亂數讀取 result_count 筆所有符合開獎結果
            // 把所有結果組成很長的字串透過socket回傳 > temp_target_amount_results
            // target_amount_results[rand_num] : 1-3-7-2-9-4-10-8-5-6,0.000000\n
            // target_amount_results[rand_num] : {獎號},{金額}\n
            // temp_target_amount_results : {獎號},{金額}\n{獎號},{金額}\n{獎號},{金額}\n{獎號},{金額}\n{獎號},{金額}\n{獎號},{金額}\n{獎號},{金額}\n
            int rand_num = 0;
            time_t t;
            char temp_target_amount_results[MAX_SOURCE_SIZE];
            memset(temp_target_amount_results, '\0', MAX_SOURCE_SIZE);
            log_info("randam %d data to temp_target_amount_results array.", resultLength);
            if( target_amount_counter > 0)
            {
                srand((unsigned) time(&t));
                for( int i = 0 ; i <= resultLength-1 ; i++ ) {
                    rand_num = rand() % target_amount_counter;
    #ifdef DEBUG
                    log_debug("rand_num[%d] = %d, target_amount_results[%d] = %s",  i, rand_num, rand_num, target_amount_results[rand_num]);
    #endif
                    //檢查重複獎號，重複則不要回傳
                    if(strstr(temp_target_amount_results, target_amount_results[rand_num]) == NULL)
                    {
                        strcat (temp_target_amount_results, target_amount_results[rand_num]);
                    }
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

            //send(forClientSockfd, "DATA,OK", sizeof("DATA,OK"), 0);
            send(forClientSockfd, temp_target_amount_results, sizeof(temp_target_amount_results), 0);
            recvBufferSize = MAX_BUFFER_SIZE;
            log_info("send back LEN process done!");
        }
        
        if(recvRows)
            free(recvRows);
        if(recvBuffer)
            free(recvBuffer);
    }

    exit(EXIT_SUCCESS);
}