
#include "../header/dateTime.h"

// GetDate - 獲取當前系統日期
/**
 *  函式名稱：GetDate
 *  功能描述：取當前系統日期
 *
 *  輸出引數：char * psDate  - 系統日期，格式為yyymmdd
 *  返回結果：0 -> 成功
 */
int GetDate(char * psDate)
{
    time_t nSeconds;
    struct tm * pTM;
    
    time(&nSeconds); // 同 nSeconds = time(NULL);
    pTM = localtime(&nSeconds);
    
    /* 系統日期,格式:YYYMMDD */
    sprintf(psDate,"%04d-%02d-%02d", 
            pTM->tm_year + 1900, pTM->tm_mon + 1, pTM->tm_mday);
    
    return 0;
}

// GetTime  - 獲取當前系統時間
/**
 *  函式名稱：GetTime
 *  功能描述：取當前系統時間
 *
 *  輸出引數：char * psTime -- 系統時間，格式為HHMMSS
 *  返回結果：0 -> 成功
 */
int GetTime(char * psTime) 
{
    time_t nSeconds;
    struct tm * pTM;
    
    time(&nSeconds);
    pTM = localtime(&nSeconds);
    
    /* 系統時間，格式: HHMMSS */
    sprintf(psTime, "%02d:%02d:%02d",
            pTM->tm_hour, pTM->tm_min, pTM->tm_sec);
           
    return 0;       
}

// GetDateTime - 取當前系統日期和時間
/**
 *  函式名稱：GetDateTime
 *  功能描述：取當前系統日期和時間
 *
 *  輸出引數：char * psDateTime -- 系統日期時間,格式為yyymmddHHMMSS
 *  返回結果：0 -> 成功
 */
int GetDateTime(char * psDateTime)
{
    time_t nSeconds;
    struct tm * pTM;
    
    time(&nSeconds);
    pTM = localtime(&nSeconds);

    /* 系統日期和時間,格式: yyyymmddHHMMSS */
    sprintf(psDateTime, "%04d-%02d-%02d %02d:%02d:%02d",
            pTM->tm_year + 1900, pTM->tm_mon + 1, pTM->tm_mday,
            pTM->tm_hour, pTM->tm_min, pTM->tm_sec);
            
    return 0;
}