#ifndef COMMON_H_   /* Include guard */
#define COMMON_H_

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include <getopt.h>
#include <sys/types.h>
//for socket
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
//for thread
#include <pthread.h>

#define _GNU_SOURCE
#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#define VERSION "1.01"
//Constants
#define MAX_SOURCE_SIZE (0x100000)
#define MAX_DEVICE_SIZE 256
#define MAX_LENGTH 255
#define MAX_BUFFER_SIZE 1000
#define SOCKET_PORT 8700
#define _DATETIME_SIZE 32
#define OPENCODE_SAMPLE "1-2-3-4-5-6-7-8-9-10"

typedef unsigned char boolean; /* Boolean value type. */
typedef unsigned long int uint32; /* Unsigned 32 bit value */
typedef unsigned short uint16; /* Unsigned 16 bit value */
typedef unsigned char uint8; /* Unsigned 8 bit value */

typedef signed long int int32; /* Signed 32 bit value */
typedef signed short int16; /* Signed 16 bit value */
typedef signed char int8; /* Signed 8 bit value */
void CL_CALLBACK contextCallback(const char * errInfo, const void * private_info, size_t cb, void * user_data);

#endif