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
int load_opnecode_answer_table(char* opencode_answer_path, char*** opencode_list, cl_uchar** opencode_answer_table);
int strCharCount(char *str, char c);
int strSplit(char *str, char *delim, char*** list);
int contains(char *str, char** list, int len);
int load_beton_list(char* path, char*** beton_list);
#endif