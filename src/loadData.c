#include "../header/loadData.h"

int loadBetonList()
{
    log_debug("check beton list file %s", gBetonListPath);
    if(!exists(gBetonListPath))
    {
        log_error("Can't find beton list file...(%s)", gBetonListPath);
        exit(EXIT_SUCCESS);
    }

    gBetonLenght = loadListFromFile(gBetonListPath, NULL);
    gBetonList = (char**)malloc(sizeof(char*) * gBetonLenght);
    loadListFromFile(gBetonListPath, &gBetonList);
    log_debug("gBetonList[%d]=%s", 0, gBetonList[0]);
    log_debug("gBetonList[%d]=%s", 1, gBetonList[1]);
    log_debug("gBetonList[%d]=%s", gBetonLenght-2, gBetonList[gBetonLenght-2]);
    log_debug("gBetonList[%d]=%s", gBetonLenght-1, gBetonList[gBetonLenght-1]);
    return gBetonLenght;
}

int loadOpencodeList()
{
    log_debug("check opencode list file %s", gOpencodeListPath);
    if(!exists(gOpencodeListPath))
    {
        log_error("Can't find opencode list file...(%s)", gOpencodeListPath);
        exit(EXIT_SUCCESS);
    }
    
    gOpencodeLenght = loadListFromFile(gOpencodeListPath, NULL);
    log_info("gOpencodeLenght=%u", gOpencodeLenght);

    gOpencodeList = (char**)malloc(sizeof(char*) * gOpencodeLenght);
    loadListFromFile(gOpencodeListPath, &gOpencodeList);

    log_debug("gOpencodeList[%d]=%s", 0, gOpencodeList[0]);
    log_debug("gOpencodeList[%d]=%s", 1, gOpencodeList[1]);
    log_debug("gOpencodeList[%d]=%s", gOpencodeLenght-2, gOpencodeList[gOpencodeLenght-2]);
    log_debug("gOpencodeList[%d]=%s", gOpencodeLenght-1, gOpencodeList[gOpencodeLenght-1]);

    return gOpencodeLenght;
}

int loadOpencodeAnswerTableVector(cl_uchar* opencodeAnswerTableVector, char* opencodeList[], const char* path)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int columnIndex = 0;
    int rowIndex = 0;
    uint32 opencode_answer_index = 0;
    clock_t timeStart, timeEnd;
    int opencodeListIndex = 0;
    unsigned long long opencodeAnswerTableIndex = 0;

    int opencodeLength = strlen(gOpencodeList[0]);
    //log_debug("opencode length:%d", opencodeLength );

    timeStart = clock();
    fp = fopen(path, "r");
    if (fp == NULL){
        log_error("read file failed: %ld", (long)fp);
        log_error("Error no is : %d\n", errno);
        log_error("Error description is : %s",strerror(errno));
        exit(EXIT_FAILURE);
    }
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;

        if (rowIndex > 0) //header不要
        {
            p = NULL;
            columnIndex = 0;
            for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
            {
                if(columnIndex == 0){
                    // Load opencode list 
                    // 把csv檔案的第1欄opencode存到opencode_list
                    opencodeListIndex = rowIndex - 1;
                    //*(opencodeList + opencodeListIndex) = (char*) malloc(sizeof(char) * (opencodeLength + 1));
                    opencodeList[opencodeListIndex] = (char*)calloc(opencodeLength + 1, sizeof(char));
                    //opencodeList[opencodeListIndex] = (char*) malloc(sizeof(char) * (opencodeLength + 1));
                    //memset(*(opencodeList + opencodeListIndex) , '\0', sizeof(char) * (opencodeLength + 1));
                    //strcpy(opencodeList[opencodeListIndex], p);
                    opencodeList[opencodeListIndex] = p;
                    //printf("opencodeList[%d]= %s \n", opencodeListIndex, opencodeList[opencodeListIndex]);
                    //log_debug("opencodeList[%d]=%s",  opencodeListIndex, opencodeList[opencodeListIndex]);
                }
                else
                {
                    //printf("%s, ", p);
                    // 把csv檔案第1欄後面的答案存到opencode_answer
                    short ret = strtol(p, NULL, 10);
                    opencodeAnswerTableVector[opencodeAnswerTableIndex] = 0;
                    if( ret == 1)
                    {
                        opencodeAnswerTableVector[opencodeAnswerTableIndex] = 'W';  //玩家贏 ASCII:87
                        opencodeAnswerTableIndex ++;
                    }
                    else if( ret == 0)
                    {   
                        opencodeAnswerTableVector[opencodeAnswerTableIndex] = 'T'; // 和 (不算輸贏) ASCII:84
                        opencodeAnswerTableIndex ++;
                    }
                    else if( ret == -1)
                    {
                       
                        opencodeAnswerTableVector[opencodeAnswerTableIndex] = 'L';  //玩家輸 ASCII:76
                        opencodeAnswerTableIndex ++;
                    }
                    //opencodeAnswerTable[opencodeAnswerTableIndex] = ret;
                    //printf("p=%s, opencodeAnswerTableVector[%d]=%s\n", p, opencodeAnswerTableIndex, opencodeAnswerTableVector[opencodeAnswerTableIndex]);
                    //opencodeAnswerTableIndex ++;
                }
                columnIndex ++;
            }
            //printf("\n");
            //log_debug("==========>rowIndex:%d, column length:%d, opencodeAnswerTableIndex=%llu",  rowIndex, columnIndex-1, opencodeAnswerTableIndex);
        }
        rowIndex++;
        line = NULL;
    }
    
    log_debug("==========>opencodeAnswerTableIndex=%llu", opencodeAnswerTableIndex);
    fclose(fp);
    timeEnd = clock();
    log_trace("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
    return rowIndex -1; //header不要
}

int loadListFromFile(const char* path, char*** list)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    int rowIndex = 0;

    fp = fopen(path, "r");
    if (fp == NULL){
        log_error("read file failed: %ld\n", (long)fp);
        exit(EXIT_FAILURE);
    }
    
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;
        
        if(list){
            *(*list + rowIndex) = (char*) malloc(sizeof(char) * (strlen(line) + 1));
            memset(*(*list + rowIndex), '\0', sizeof(char) * (strlen(line) + 1));
            strncpy(*(*list + rowIndex), line, (strlen(line) - 2)); //不要結尾的'\n'斷行
            //printf("rowIndex=%d, beton=%s, len=%d<=====\n", rowIndex, *(*list + rowIndex), strlen(*(*list + rowIndex)));
        }
        rowIndex++;
    }

    fclose(fp);
    if (line)
        free(line);
    return rowIndex; //header不要
}

int betsAmountVectorAppend(
    cl_float*       betsAmountVector, 
    cl_float*       betsAmountWithOddsVector,
    int             startIndex,
    const char*    bets[], 
    const char*    odds[], 
    float           unitAmount, 
    int             len)
{
    int odds_index = 0;
    for(int i=0; i<=gBetonLenght-1; i++)
    {
        if(contains(gBetonList[i], bets, len) == 1)
        {
            betsAmountVector[startIndex + i] = unitAmount;
            float tmp_odds = strtof(odds[odds_index], NULL);
            betsAmountWithOddsVector[startIndex + i] = (tmp_odds - 1) * unitAmount; //此處賠率要扣掉1（本金
            odds_index ++;
            /*
            log_debug("========> betsAmountVector[%d]=%f, betsAmountWithOddsVector[%d]=%f ", 
                startIndex + i, betsAmountVector[startIndex + i] ,
                startIndex + i, betsAmountWithOddsVector[startIndex + i]);
                */
        }
        else
        {
            betsAmountVector[startIndex + i] = 0;
            betsAmountWithOddsVector[startIndex + i] = 0;
        }
    }
    return 0;
}

int loadParmeters(
    int*        wagerLength, 
    char**      expectId, 
    int*        direction, 
    float*      killRate,
    int*        resultLength,
    const char* strRawData)
{   
    int columnLength = count(strRawData, '|') + 1;
    char** columns = (char**)malloc(sizeof(char*) * columnLength);
    split(columns, strRawData, "|");
    *wagerLength = strtol(columns[0], NULL, 10);   //0: wager_length
    strcpy(expectId, columns[1]);                   //1: expectId
    *direction = strtol(columns[2], NULL, 10);      //2: direction
    *killRate = strtof(columns[3], NULL);           //2: killRate
    *resultLength = strtol(columns[4], NULL, 10);  //4: result_length

    if(columns)
        free(columns);
    return 0;
}


int loadRowData2BetsAmountVector(
    cl_float*       betsAmountVector,
    cl_float*       betsAmountWithOddsVector,
    float*          totalBetsAmount,
    const char*     rawDatalist[],
    int             rawDatalistLength)
{
    int recvColumnLength = 0;
    char** recvColumns;
    *totalBetsAmount = 0;
    int index = 0;
    for(int i=0; i<=rawDatalistLength-1; i++)
    {
        //log_debug("recvRows[%d]=%s", i, rawDatalist[i]);
        recvColumnLength = count(rawDatalist[i], '|') + 1;
        recvColumns = (char**)malloc(sizeof(char*) * recvColumnLength + 1);
        split(recvColumns, rawDatalist[i], "|");

        //recvColumns[0]: 下注內容
        int betsLength = count(recvColumns[0], ',') + 1;
        char** bets = (char**)malloc(sizeof(char*) * betsLength);
        split(bets, recvColumns[0], ",");
        log_debug("bets[0]=%s", bets[0]);
        log_debug("bets[%d]=%s", betsLength -1, bets[betsLength-1]);
        
        //recvColumns[1]: 下注賠率
        int oddsLength = count(recvColumns[1], ',') + 1;
        char** odds = (char**)malloc(sizeof(char*) * oddsLength);
        split(odds, recvColumns[1], ","); 
        log_debug("odds[0]=%s", odds[0]);
        log_debug("odds[%d]=%s", oddsLength -1, odds[oddsLength-1]);

        //recvColumns[2]: 單注金額
        float unitAmount = strtof(recvColumns[2], NULL);
        log_debug("unitAmount=%f", unitAmount);

        for(int j=0; j<=betsLength-1; j++ )
        {
            *totalBetsAmount += unitAmount;
        }
        
        log_debug("start index = %d", index);
        betsAmountVectorAppend(betsAmountVector, betsAmountWithOddsVector, index, bets, odds, unitAmount, betsLength);
        index += gBetonLenght;
    }  
    return 0;
}

int loadConfigFromJsonFile(const char* lotteryKind)
{
    int ret = 0;
    const char appPath[PATH_MAX];
    const char appFoder[PATH_MAX];
    memset(appPath, '\0', PATH_MAX);
    memset(appFoder, '\0', PATH_MAX);
    ssize_t count = readlink("/proc/self/exe", appPath, PATH_MAX);
    if (count != -1) {
        printf("APP PATH=%s\n", appPath);
        strcpy(appFoder, dirname(appPath));
        printf("APP Folder=%s\n", appFoder); //後面有帶 bin/
    }

    char* workerFolder = substring(appFoder, 0, strlen(appFoder) -3);
    printf("workerFolder= %s\n", workerFolder);
    strcpy(gWorkerFolder, workerFolder);
   
    char configName[MAX_LENGTH];
    memset(configName, '\0', MAX_LENGTH);
    sprintf(configName, "%s_config.json", lotteryKind);
    printf("config Name : %s\n", configName);

    char configPath[PATH_MAX];
    memset(configPath, '\0', PATH_MAX);
    pathCombine(configPath, appFoder, configName);
    //printf("load config file : %s\n", configPath);

    if(exists(configPath) != 1)
    {
        printf("can't find %s\n", configPath);
        return -1;
    }

	json_object *test_obj = NULL;
	json_object *tmp_obj = NULL;
	json_object *tmp1_obj = NULL;
	json_object *tmp2_obj = NULL;

    //get json object from file
	test_obj = json_object_from_file(configPath);
	if (!test_obj)
	{
		printf("Cannot open %s\n", configPath);
		ret = -1;
		goto error;
	}
    //==============================================
    //get array
	tmp_obj = json_object_object_get(test_obj, "OPENCODE_ANSWER_TABLE_PATH");
	if (!tmp_obj)
	{
		printf("Cannot get %s object\n", "OPENCODE_ANSWER_TABLE_PATH");
		ret = -1;
		goto error;
	}
	//get the length of the array
	//printf("%s size = %d\n", "OPENCODE_ANSWER_TABLE_PATH", json_object_array_length(tmp_obj));

	//get the value of array[0]
	tmp1_obj = json_object_array_get_idx(tmp_obj, 0);
    pathCombine(gOpencodeAnswerTablePath[0], gWorkerFolder, json_object_get_string(tmp1_obj));
	//printf("%s[0] = %s\n", "OPENCODE_ANSWER_TABLE_PATH[0]", gOpencodeAnswerTablePath[0]);

	//get the value of array[1]
	tmp1_obj = json_object_array_get_idx(tmp_obj, 1);
    pathCombine(gOpencodeAnswerTablePath[1],  gWorkerFolder , json_object_get_string(tmp1_obj));
	//printf("%s[1] = %s\n", "OPENCODE_ANSWER_TABLE_PATH[1]",gOpencodeAnswerTablePath[1]);
    //==============================================
    tmp_obj = json_object_object_get(test_obj, "BETON_LIST_PATH");
	if (!tmp_obj)
	{
		printf("Cannot get %s object\n", "BETON_LIST_PATH");
		ret = -1;
		goto error;
	}
    pathCombine(gBetonListPath , gWorkerFolder, json_object_get_string(tmp_obj));
	//printf("BETON_LIST_PATH = %s\n",gBetonListPath);
    //==============================================
    tmp_obj = json_object_object_get(test_obj, "OPENCODE_LIST_PATH");
	if (!tmp_obj)
	{
		printf("Cannot get %s object\n", "OPENCODE_LIST_PATH");
		ret = -1;
		goto error;
	}
    pathCombine(gOpencodeListPath,  gWorkerFolder , json_object_get_string(tmp_obj));
	//printf("OPENCODE_LIST_PATH = %s\n", gOpencodeListPath);
    //==============================================
    tmp_obj = json_object_object_get(test_obj, "KERNEL_PATH");
	if (!tmp_obj)
	{
		printf("Cannot get %s object\n", "KERNEL_PATH");
		ret = -1;
		goto error;
	}
    pathCombine(gKernelPath , gWorkerFolder, json_object_get_string(tmp_obj));
	//printf("KERNEL_PATH = %s\n", gKernelPath);
    //==============================================
    tmp_obj = json_object_object_get(test_obj, "LOG_PATH");
	if (!tmp_obj)
	{
		printf("Cannot get %s object\n", "LOG_PATH");
		ret = -1;
		goto error;
	}
    pathCombine(gLogPath , gWorkerFolder, json_object_get_string(tmp_obj));
	//printf("LOG_PATH = %s\n", gLogPath);
    //==============================================
    //get integer
	tmp_obj = json_object_object_get(test_obj, "SOCKET_PORT");
	if (!tmp_obj)
	{
		printf("Cannot get %s object\n", "SOCKET_PORT");
		ret = -1;
		goto error;
	}
    gSocketPort = json_object_get_int(tmp_obj);
	//printf("SOCKET_PORT = %d\n", gSocketPort);

error:
	json_object_put(test_obj);

	return ret;
}

int loadWagerLengthFromJsonFile(int* wagerLength, const char* jsonfile)
{
    int ret = 0;
    json_object* json_obj =NULL;
    json_object *tmp_obj = NULL;

    json_obj = json_object_from_file(jsonfile);
    if (!json_obj)
    {
        log_error("Cannot open %s", jsonfile);
        ret = -1;
        goto error;
    }

    //讀取wager_length
    //===============================================
    tmp_obj = json_object_object_get(json_obj, "wager_length");
    if (!tmp_obj)
    {
        log_error("Cannot get %s object", "wager_length");
        ret = -1;
        goto error;
    }
    *wagerLength = json_object_get_int(tmp_obj);
    log_trace("%s = %d", "wager_length", *wagerLength);
error:
	json_object_put(json_obj);

	return ret;
}

int loadParmetersFromJsonFile(    
    int*      wagerLength, 
    char**      expectId, 
    int*        direction, 
    float*      killRate,
    int*        resultLength,
    float*     totalBetsAmount,
    cl_float* betsAmountVector,
    cl_float* betsAmountWithOddsVector,
    const char* jsonfile)
{
    int ret = 0;
    json_object* json_obj =NULL;
    json_object *tmp_obj = NULL;
    json_object *bets_arr_obj = NULL;

    json_object *bets_betons_index_obj = NULL;
    json_object *betons_arr_obj = NULL;
    json_object *betons_obj = NULL;
    
    json_object *bets_odds_index_obj = NULL;
    json_object *odds_arr_obj = NULL;
    json_object *odds_obj = NULL;

    json_object *bets_unitAmount_index_obj = NULL;
    json_object *unitAmount_obj = NULL;

    float unitAmount = 0;
    char** bets = NULL;
    float* odds = NULL;
    char* beton = NULL;

    json_obj = json_object_from_file(jsonfile);
    if (!json_obj)
    {
        log_error("Cannot open %s", jsonfile);
        ret = -1;
        goto error;
    }

    //讀取wager_length
    //===============================================
    tmp_obj = json_object_object_get(json_obj, "wager_length");
    if (!tmp_obj)
    {
        log_error("Cannot get %s object", "wager_length");
        ret = -1;
        goto error;
    }
    *wagerLength = json_object_get_int(tmp_obj);
    log_trace("%s = %d", "wager_length", *wagerLength);

    //讀取 expectId
    //===============================================
    tmp_obj = json_object_object_get(json_obj, "expectId");
    if (!tmp_obj)
    {
        log_error("Cannot get %s object", "expectId");
        ret = -1;
        goto error;
    }
    strcpy(expectId,  json_object_get_string(tmp_obj));
    log_trace("%s = %s", "expectId", expectId);

    //讀取 direction
    //===============================================
    tmp_obj = json_object_object_get(json_obj, "direction");
    if (!tmp_obj)
    {
        log_error("Cannot get %s object", "direction");
        ret = -1;
        goto error;
    }
    *direction = json_object_get_int(tmp_obj);
    log_trace("%s = %d", "direction", *direction);

    //讀取 killRate
    //===============================================
    tmp_obj = json_object_object_get(json_obj, "killRate");
    if (!tmp_obj)
    {
        log_error("Cannot get %s object", "killRate");
        ret = -1;
        goto error;
    }
    *killRate = json_object_get_double(tmp_obj);
    log_trace("%s = %F", "killRate", *killRate);

    //讀取 opencodeCount
    //===============================================
    tmp_obj = json_object_object_get(json_obj, "opencodeCount");
    if (!tmp_obj)
    {
        log_error("Cannot get %s object", "opencodeCount");
        ret = -1;
        goto error;
    }
    *resultLength = json_object_get_int(tmp_obj);
    log_trace("%s = %d", "resultLength", *resultLength);

    //讀取 Bets array
    //===============================================
    bets_arr_obj = json_object_object_get(json_obj, "Bets");
    if (!bets_arr_obj)
    {
        log_error("Cannot get %s object", "Bets");
        ret = -1;
        goto error;
    }
    //get the length of the array
    int bets_length = json_object_array_length(bets_arr_obj);
    log_trace("%s size = %d", "Bets", bets_length);

    int startIndex = 0;
    *totalBetsAmount = 0;
    for (int i=0 ; i<= bets_length-1 ; i++ )
    {
        //取得 betons array 物件
        //=======================================
        bets_betons_index_obj = json_object_array_get_idx(bets_arr_obj, i);
        betons_arr_obj = json_object_object_get(bets_betons_index_obj, "betons");
        int betons_length = json_object_array_length(betons_arr_obj);
        //printf("%s size = %d\n", "betons", betons_length);

        //取得 odds array 物件
        //=======================================
        bets_odds_index_obj = json_object_array_get_idx(bets_arr_obj, i);
        odds_arr_obj = json_object_object_get(bets_odds_index_obj, "odds");
        int odds_length = json_object_array_length(odds_arr_obj);
        //printf("%s size = %d\n", "odds", odds_length);

        //unitAmount
        //=======================================
        bets_unitAmount_index_obj = json_object_array_get_idx(bets_arr_obj, i);
        unitAmount_obj = json_object_object_get(bets_unitAmount_index_obj, "unitAmount");
        float unitAmount =  json_object_get_double(unitAmount_obj);
        printf("%s = %F\n", "unitAmount", unitAmount);
        
        //讀取 betons array 
        //讀取 odds array 
        //=======================================
        bets = (char**)malloc(sizeof(char*) * betons_length);
        odds = (float*)malloc(sizeof(float) * odds_length);
        beton = NULL;
        for(int j=0; j<= betons_length-1; j++ )
        {
            betons_obj = json_object_array_get_idx(betons_arr_obj, j);
            beton = json_object_get_string(betons_obj);
            //bets[j] = (char*)malloc(sizeof(char) * strlen(beton));
            bets[j] = json_object_get_string(betons_obj);

            odds_obj = json_object_array_get_idx(odds_arr_obj, j);
            odds[j] = json_object_get_double(odds_obj);
            printf("====>betons[%d]=%s, odds[%d]=%F \n",  j, bets[j], j, odds[j]);              

            *totalBetsAmount += unitAmount;
        }

        //========================================================================
        int odds_index = 0;
        for(int i=0; i<=gBetonLenght-1; i++)
        {
            if(contains(gBetonList[i], bets, betons_length) == 1)
            {
                betsAmountVector[startIndex + i] = unitAmount;
                printf("betsAmountVector[%d]=%f\n", startIndex + i,  betsAmountVector[startIndex + i]);
                betsAmountWithOddsVector[startIndex + i] = (odds[odds_index] - 1) * unitAmount; //此處賠率要扣掉1（本金
                odds_index ++;
            }
            else
            {
                betsAmountVector[startIndex + i] = 0;
                betsAmountWithOddsVector[startIndex + i] = 0;
            }
        }
        startIndex += gBetonLenght;
        //========================================================================

        //Release alloc memory
        //========================================================================
        /*
        for(int j=0; j<= betons_length-1; j++ )
        {
            if(bets[j])
            {
                log_debug("Release bets[%d] pointer", j);
                bets[j] = NULL;
            }
        }*/
        if(bets){
            log_debug("Release bets pointer");
            free(bets);
        }
        if(odds){
            log_debug("Release odds pointer");
            free(odds);
        }
    }
error:
	json_object_put(json_obj);

	return ret;
}