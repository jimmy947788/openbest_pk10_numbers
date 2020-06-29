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

#define _GNU_SOURCE
#ifdef __APPLE__
#include <OpenCL/opencl.h>
#else
#include <CL/cl.h>
#endif

#define VERSION "1.00"
//Constants
#define MAX_SOURCE_SIZE (0x100000)
#define MAX_DEVICE_SIZE 256

void CL_CALLBACK contextCallback(const char * errInfo, const void * private_info, size_t cb, void * user_data);

/*
cl_command_queue queue;
cl_program program = NULL;
cl_kernel kernel_sum_beton_total_amount = NULL;
cl_kernel kernel_calc_numbers_risk = NULL;
int platformId = 0; */

#endif