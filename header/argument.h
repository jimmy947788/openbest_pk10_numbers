
#include <getopt.h>
#include <unistd.h>
#include <string.h>
#include "mytype.h"
#include "config.h"
#include "utility.h"

#ifndef ARGUMENT_H_   /* Include guard */
#define ARGUMENT_H_

void help();
void laod_args(int argc, char* argv[], 
        char kernel_program_file[], 
        char work_folder[], 
        char log_dir[]);
#endif