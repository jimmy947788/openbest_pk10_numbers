#include "config.h"
#include <linux/limits.h>   // PATH_MAX

#ifndef COMMON_H_   /* Include guard */
#define COMMON_H_

char     gWorkerFolder[PATH_MAX];
char**   gBetonList;
uint32      gBetonLenght;

char**   gOpencodeList;
uint32      gOpencodeLenght;

uint32 GPU_HANDEL_COUNT[USE_GPU_NUM];

char     gKernelPath[PATH_MAX];
char     gLogPath[PATH_MAX];
char     gBetonListPath[PATH_MAX];
char     gOpencodeListPath[PATH_MAX];
char     gOpencodeAnswerTablePath[USE_GPU_NUM][PATH_MAX];
uint32  gSocketPort;
#endif