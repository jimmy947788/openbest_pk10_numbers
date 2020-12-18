#include "mytype.h"

#ifndef CONFIG_H_   /* Include guard */
#define CONFIG_H_

//Constants
#define MAX_SOURCE_SIZE (0x100000)
#define MAX_DEVICE_SIZE 256
#define MAX_LENGTH 255
#define MAX_BUFFER_SIZE 1000
#define SOCKET_PORT 8700
#define _DATETIME_SIZE 32
#define USE_GPU_NUM 2
#define VERSION "1.01"


#ifdef PK10
    static const char OPENCODE_SAMPLE[] ="1-2-3-4-5-6-7-8-9-10";
#elif defined SSC 
    static const char OPENCODE_SAMPLE[] ="1-2-3-4-5";
#endif

#ifdef PK10
    #define BETON_COUNT 1060
    #define OPENCODE_COUNT 3628800
#elif defined SSC 
    #define BETON_COUNT 10705  //117662
    #define OPENCODE_COUNT 100000
#endif

static const char OPENCODE_ANSWER_TABLE_PATH[USE_GPU_NUM][MAX_LENGTH] = {
    #ifdef PK10
        "/data/pk10_opencode_table_1.csv",
        "/data/pk10_opencode_table_2.csv"
    #elif defined SSC 
        "/data/ssc_opencode_table_1.csv",
        "/data/ssc_opencode_table_2.csv"
    #endif
};

static const uint32 GPU_HANDEL_COUNT[USE_GPU_NUM] = {
    BETON_COUNT / USE_GPU_NUM,
    OPENCODE_COUNT / USE_GPU_NUM,
};

#endif