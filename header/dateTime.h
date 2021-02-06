
#ifndef DATETIME_H_   /* Include guard */
#define DATETIME_H_

#include <time.h>


// GetDate - 獲取當前系統日期
/**
 *  函式名稱：GetDate
 *  功能描述：取當前系統日期
 *
 *  輸出引數：char * psDate  - 系統日期，格式為yyymmdd
 *  返回結果：0 -> 成功
 */
int GetDate(char * psDate);

// GetTime  - 獲取當前系統時間
/**
 *  函式名稱：GetTime
 *  功能描述：取當前系統時間
 *
 *  輸出引數：char * psTime -- 系統時間，格式為HHMMSS
 *  返回結果：0 -> 成功
 */
int GetTime(char * psTime);


// GetDateTime - 取當前系統日期和時間
/**
 *  函式名稱：GetDateTime
 *  功能描述：取當前系統日期和時間
 *
 *  輸出引數：char * psDateTime -- 系統日期時間,格式為yyymmddHHMMSS
 *  返回結果：0 -> 成功
 */
int GetDateTime(char * psDateTime);
#endif