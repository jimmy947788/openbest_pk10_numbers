#include "mytype.h"

#ifndef CONFIG_H_   /* Include guard */
#define CONFIG_H_

//Constants
#define MAX_SOURCE_SIZE (0x100000)
#define MAX_DEVICE_SIZE 256
#define MAX_LENGTH 255
#define MAX_BUFFER_SIZE 1024
#define SOCKET_PORT 8700
#define _DATETIME_SIZE 32
#define USE_GPU_NUM 2
#define VERSION "1.30"

/*
#ifdef PK10
    static const char OPENCODE_SAMPLE[] ="1-2-3-4-5-6-7-8-9-10";
#elif defined SSC 
    static const char OPENCODE_SAMPLE[] ="1-2-3-4-5";
#elif defined llX5 
    static const char OPENCODE_SAMPLE[] ="1-2-3-4-5";
#elif defined K3 
    static const char OPENCODE_SAMPLE[] ="1-2-3";
#endif

static const char OPENCODE_ANSWER_TABLE_PATH[USE_GPU_NUM][MAX_LENGTH] = {
    #ifdef PK10
        "/data/pk10_opencode_table_1.csv",
        "/data/pk10_opencode_table_2.csv"
    #elif defined SSC 
        "/data/ssc_opencode_table_1.csv",
        "/data/ssc_opencode_table_2.csv"
    #elif defined llX5 
        "/data/11x5_opencode_table_1.csv",
        "/data/11x5_opencode_table_2.csv"
    #elif defined K3 
        "/data/k3_opencode_table_1.csv",
        "/data/k3_opencode_table_2.csv"
    #endif
};

static const char BETON_LIST_PATH[] = {
    #ifdef PK10
        "data/pk10_beton_list.txt",
    #elif defined SSC 
        "data/ssc_beton_list.txt",
    #elif defined llX5 
        "data/11x5_beton_list.txt",
    #elif defined K3
        "data/k3_beton_list.txt",
    #endif
};

static const char OPENCODE_LIST_PATH[] = {
    #ifdef PK10
        "data/pk10_opencode_list.txt",
    #elif defined SSC 
        "data/ssc_opencode_list.txt",
    #elif defined llX5 
        "data/11x5_opencode_list.txt",
    #elif defined K3 
        "data/k3_opencode_list.txt",
    #endif
};
*/
#endif