#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>
#include "utility.h"
#include "config.h"
#include "dateTime.h"
#include "mytype.h"
#include "myfile.h"
#include "mystring.h"
#include "logger.h"

#ifndef LOADDATA_H_   /* Include guard */
#define LOADDATA_H_

/** 
 * @brief 讀取TXT檔案到陣列。每一行一筆資料，最後一行要是空資料。
 * @note  
 * @param path:[IN] TXT檔案完整路徑
 * @param list:[OUT] 保存資料用陣列。（傳入NULL則只回傳資料比數）
 * @retval 傳資料比數
 */
int loadListFromFile(const char* path, char*** list);

int loadBetonList();
int loadOpencodeList();
int loadOpencodeAnswerTable(cl_uchar* opencodeAnswerTable, char*** opencodeList, const char* path);

/** 
 * @brief 轉換注單和賠率變成成opencl要處理的matrix  
 * @note   
 * @param betsAmountOnehot:[OUT] 包含所有beton的一維陣列，有下注內容是[單注金額]未下注內容是0。
 * @param betsAmountWithOddsOnehot:[OUT] 包含所有beton的一維陣列，有下注內容是[單注金額] * [賠率]未下注內容是0。
 * @param startIndex:[IN] Onehot起始位址 
 * @param bets:[IN]所下注的玩法陣列 
 * @param odds:[IN]所下注的賠率陣列
 * @param unitAmount:[IN]單注金額
 * @param len:[IN]玩法&賠率陣列長度
 * @retval None
 */
int bets2onehot(
    cl_float*       betsAmountOnehot, 
    cl_float*       betsAmountWithOddsOnehot,
    int             startIndex,
    const char**    bets, 
    const char**    odds, 
    float           unitAmount, 
    int             len);

/**
 * @brief 把web傳過來的字串讀取出來運算用參數
 * @note 
 * @param wagerLength: [OUT] 注單數量
 * @param expectId: [OUT] 期號
 * @param direction: [OUT] 找尋方向
 * @param killRate: [OUT] 殺率
 * @param resultLength: [OUT] 取得有有效獎號數量
 * @param strRawData:[IN]web傳過來的字串（請移除"DATA:"，"LEN:"... ）
 * @retval None
 */
int loadParmeters(
    int*        wagerLength, 
    char**      expectId, 
    int*        direction, 
    float*      killRate,
    int*        resultLength,
    const char* strRawData);


int loadBetsAmountOnehot(
    cl_float*       betsAmountOnehot,
    cl_float*       betsAmountWithOddsOnehot,
    float*          totalBetsAmount,
    const char**    rawDatalist,
    int             rawDatalistLength);
#endif