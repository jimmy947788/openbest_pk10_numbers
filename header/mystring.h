
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include "config.h"
#include "common.h"
#include "logger.h"

#ifndef MYSTRING_H_   /* Include guard */
#define MYSTRING_H_

/** 
 * @brief 計算字元在字串裡面出現得次數。
 * @note  
 * @param path:[IN] 被搜尋的字串
 * @param list:[IN] 要搜尋的字元
 * @retval 字元出現次數
 */
int strCharCount(const char *str, char c);

/** 
 * @brief 分割字串到陣列。
 * @note  
 * @param list:[OUT] 保存資料的陣列
 * @param str:[IN] 要被分割的字串
 * @param delim:[IN] 分割的字元
 * @retval 陣列的長度
 */
int split(char* list[], const char str[], const char delim[]);

/** 
 * @brief 檢查字串是否存在陣列。
 * @note  
 * @param str:[IN] 要搜尋的字串
 * @param list:[IN] 比對的陣列
 * @param len:[IN] 陣列長度
 * @retval 1:存在 2.不存在 
 */
int contains(const char str[], const  char* list[], int len);

/** 
 * @brief 擷取字串。
 * @note  
 * @param s_src:[IN] 來源字串
 * @param i_start:[IN] 起始位置
 * @param i_end:[IN] 結束位置
 * @retval 擷取後的字串
 */
char* substring(const char *s_src, int i_start, int i_end);
#endif