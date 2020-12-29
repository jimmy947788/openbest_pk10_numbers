#include <stdint.h>
#include "config.h"

#ifndef COMMON_H_   /* Include guard */
#define COMMON_H_

char        gWorkerFolder[MAX_LENGTH];
char**      gBetonList;
uint32_t    gBetonLenght;

char**      gOpencodeList;
uint32_t    gOpencodeLenght;

uint32_t GPU_HANDEL_COUNT[USE_GPU_NUM];

#endif