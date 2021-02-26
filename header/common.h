
#ifndef COMMON_H_   /* Include guard */
#define COMMON_H_

#include <linux/limits.h>   // PATH_MAX
#include "../header/mytype.h"

#define _GNU_SOURCE
#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif



#define MAX_SOURCE_SIZE (0x100000)
#define MAX_DEVICE_SIZE 256
#define MAX_LENGTH 255
#define MAX_BUFFER_SIZE 1024
#define _DATETIME_SIZE 32
#define USE_GPU_NUM 2
#define VERSION "2.30"

extern char     gWorkerFolder[PATH_MAX];
extern char**   gBetonList;
extern uint32   gBetonLenght;

extern char**   gOpencodeList;
extern uint32   gOpencodeLenght;

extern uint32 GPU_HANDEL_COUNT[USE_GPU_NUM];

extern char     gLotteryKind[MAX_LENGTH];
extern char     gKernelPath[PATH_MAX];
extern char     gLogPath[PATH_MAX];
extern char     gBetonListPath[PATH_MAX];
extern char     gOpencodeListPath[PATH_MAX];
extern char     gOpencodeAnswerTablePath[USE_GPU_NUM][PATH_MAX];
extern uint32  gSocketPort;

#endif