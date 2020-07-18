#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "utility.h"
#include "config.h"
#include "dateTime.h"
#include "mytype.h"

#ifndef LOADDATA_H_   /* Include guard */
#define LOADDATA_H_

int readFileContent(const char* path, char *content);
void load_socket_data(char* data, 
    char* beton_amount_table_file, 
    char* beton_amount_table_with_odds_file, 
    int* wager_length, 
    char* expectId,
    float* target_amount,
    float* tolerance);
void load_beton_amount_table(char* beton_amount_path, cl_float** beton_amount_table);
#endif