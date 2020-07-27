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
static const char OPENCODE_SAMPLE[] ="1-2-3-4-5-6-7-8-9-10";

#define VERSION "1.01"
#define PK10_BETON_COUNT 1056
#define PK10_OPENCODE_COUNT 3628800

#define USE_GPU_NUM 2
static const char OPENCODE_ANSWER_TABLE_PATH[USE_GPU_NUM][MAX_LENGTH] = {
    "/data/opencode_table_1.csv",
    "/data/opencode_table_2.csv"
};
static const uint32 GPU_HANDEL_COUNT[USE_GPU_NUM] = {
    PK10_OPENCODE_COUNT / USE_GPU_NUM,
    PK10_OPENCODE_COUNT / USE_GPU_NUM,
};

#endif