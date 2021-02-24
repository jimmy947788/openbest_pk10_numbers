#ifndef UTILITY_H_   /* Include guard */
#define UTILITY_H_

#include <stdio.h>
#include <time.h>
#include "common.h"
#include "loadData.h"
#include "logger.h"
#include "myfile.h"

void checkErr(cl_int err, const char* name);
void CL_CALLBACK contextCallback(const char * errInfo, const void * private_info, size_t cb, void * user_data);
void show_device_information(cl_device_id device);
cl_uint get_platforms(cl_platform_id **platforms);
cl_uint create_gpu_device_list(cl_platform_id platform, cl_device_id** device_list);
void create_queue_list(cl_context context, 
    cl_device_id* device_list, cl_int total_devices,
    cl_command_queue** queue_list);
void build_program_for_all_devices(
    char* programPath, 
    cl_context context,
    cl_device_id* device_list,
    cl_program** program);
void executionTime(cl_event event, double* elapsedTime);


int run_kernel_sum_beton_total_amount(
        const cl_context context, 
        const  cl_command_queue queue, 
        const  cl_kernel kernel,
        const  int wgaer_length, 
        const  cl_ushort* one_mask, 
        const  cl_float* bet_amount, 
        cl_float** result);

#endif