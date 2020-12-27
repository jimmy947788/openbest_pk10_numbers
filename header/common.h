#include "config.h"

#ifndef COMMON_H_   /* Include guard */
#define COMMON_H_

char     gWorkerFolder[MAX_LENGTH];
char**   gBetonList;
int      gBetonLenght;

char**   gOpencodeList;
int      gOpencodeLenght;

uint32 GPU_HANDEL_COUNT[USE_GPU_NUM];

#endif