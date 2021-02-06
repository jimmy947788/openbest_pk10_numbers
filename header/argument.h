

#ifndef ARGUMENT_H_   /* Include guard */
#define ARGUMENT_H_

#include <getopt.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include "common.h"
#include "mytype.h"

void help();
void laod_args(int argc, char* argv[], 
        char lotteryKind[]);
#endif