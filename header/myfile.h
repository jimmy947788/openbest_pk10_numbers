#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <stdlib.h>
#include "config.h"
#include "common.h"
#include "logger.h"

#ifndef MYFILE_H_   /* Include guard */
#define MYFILE_H_

/** 
 * @brief 合併檔案路徑
 * @note  
 * @param destination:[OUT] 檔案完整路徑
 * @param path1:[IN] 路徑1
 * @param path2:[IN] 路徑2
 * @retval 1:存在，2:不存在
 */
void pathCombine(char* destination, const char* path1, const char* path2);

/** 
 * @brief 檢查檔案是否存在。
 * @note  
 * @param path:[IN] 檔案完整路徑
 * @retval 1:存在，2:不存在
 */
int fileExists(const char* path);


/** 
 * @brief 讀取檔案內容
 * @note  
 * @param content:[OUT] 檔案內容
 * @param path:[IN] 檔案完整路徑
 * @retval 檔案大小
 */
int readContent(char *content, const char* path);

#endif