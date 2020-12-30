#include "../header/loadData.h"

int loadBetonList()
{
    int fullpathLength = strlen(gWorkerFolder) + strlen(BETON_LIST_PATH) + 2;
    char* fullpath = (char*)malloc(sizeof(char) * fullpathLength +1);
    memset(fullpath, '\0', sizeof(char) * fullpathLength + 1);
    pathCombine(fullpath, gWorkerFolder, BETON_LIST_PATH);

    log_debug("check beton list file %s", fullpath);
    if(!exists(fullpath))
    {
        log_error("Can't find beton list file...(%s)", fullpath);
        exit(EXIT_SUCCESS);
    }

    gBetonLenght = loadListFromFile(fullpath, NULL);
    gBetonList = (char**)malloc(sizeof(char*) * gBetonLenght);
    loadListFromFile(fullpath, &gBetonList);

    log_debug("gBetonList[%d]=%s", 0, gBetonList[0]);
    log_debug("gBetonList[%d]=%s", 1, gBetonList[1]);
    log_debug("gBetonList[%d]=%s", gBetonLenght-2, gBetonList[gBetonLenght-2]);
    log_debug("gBetonList[%d]=%s", gBetonLenght-1, gBetonList[gBetonLenght-1]);

    if(fullpath)
        free(fullpath);
    return gBetonLenght;
}

int loadOpencodeList()
{
    int fullpathLength = strlen(gWorkerFolder) + strlen(OPENCODE_LIST_PATH) + 2;
    char* fullpath = (char*)malloc(sizeof(char) * (fullpathLength + 1));
    memset(fullpath, '\0', sizeof(char) * (fullpathLength + 1));
    pathCombine(fullpath, gWorkerFolder, OPENCODE_LIST_PATH);

    log_debug("check opencode list file %s", fullpath);
    if(!exists(fullpath))
    {
        log_error("Can't find opencode list file...(%s)", fullpath);
        exit(EXIT_SUCCESS);
    }
    
    gOpencodeLenght = loadListFromFile(fullpath, NULL);
    log_debug("gOpencodeLenght=%d", gOpencodeLenght);

    gOpencodeList = (char**)malloc(sizeof(char*) * gOpencodeLenght);
    loadListFromFile(fullpath, &gOpencodeList);

    log_debug("gOpencodeList[%d]=%s", 0, gOpencodeList[0]);
    log_debug("gOpencodeList[%d]=%s", 1, gOpencodeList[1]);
    log_debug("gOpencodeList[%d]=%s", gOpencodeLenght-2, gOpencodeList[gOpencodeLenght-2]);
    log_debug("gOpencodeList[%d]=%s", gOpencodeLenght-1, gOpencodeList[gOpencodeLenght-1]);
    if(fullpath)
        free(fullpath);
    return gOpencodeLenght;
}

int loadOpencodeAnswerTableVector(cl_uchar* opencodeAnswerTableVector, char*** opencodeList, const char* path)
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

    int fullpathLength = strlen(gWorkerFolder) + strlen(path) + 2;
    char* fullpath = (char*)malloc(sizeof(char) * (fullpathLength + 1));
    memset(fullpath, '\0', sizeof(char) * (fullpathLength + 1));
    pathCombine(fullpath, gWorkerFolder, path);
    //log_info("load file full path:%s", fullpath);

    timeStart = clock();
    fp = fopen(fullpath, "r");
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
                    //*(*opencodeList + opencodeListIndex) = (char*) malloc(sizeof(char) * opencodeLength);
                    opencodeList[opencodeListIndex] = (char*) malloc(sizeof(char) * (opencodeLength + 1));
                    memset(opencodeList[opencodeListIndex], '\0', sizeof(char) * (opencodeLength + 1));
                    //strcpy(*(*opencodeList + opencodeListIndex), p);
                    strcpy(opencodeList[opencodeListIndex], p);
                    //printf("opencodeList[%d]= %s \n", opencodeListIndex, *(*opencodeList + opencodeListIndex));
                    //log_debug("opencodeList[%d]=%s",  opencodeListIndex, opencodeList[opencodeListIndex]);
                }
                else
                {
                    // 把csv檔案第1欄後面的答案存到opencode_answer
                    short ret = strtol(p, NULL, 10);
                    if(ret > 0){
                        opencodeAnswerTableVector[opencodeAnswerTableIndex] = 43;  
                    }
                    else
                    {
                        opencodeAnswerTableVector[opencodeAnswerTableIndex] = 45;  
                    }
                    
                    //opencodeAnswerTable[opencodeAnswerTableIndex] = ret;
                    //printf("opencodeAnswerTable[%d]=%d\n",opencodeAnswerTableIndex, opencodeAnswerTable[opencodeAnswerTableIndex]);
                    opencodeAnswerTableIndex ++;
                }
                columnIndex ++;
            }
            //log_debug("==========>rowIndex:%d, column length:%d, opencodeAnswerTableIndex=%llu",  rowIndex, columnIndex-1, opencodeAnswerTableIndex);
        }
        rowIndex++;
    }

    fclose(fp);
    if (line)
        free(line);
    if(fullpath)
        free(fullpath);
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
    const char**    bets, 
    const char**    odds, 
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
    const char**    rawDatalist,
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