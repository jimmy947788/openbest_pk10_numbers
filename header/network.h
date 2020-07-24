#include <stdlib.h>
#include <string.h>
//for socket
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "config.h"

#ifndef NETWORK_H_   /* Include guard */
#define NETWORK_H_

void recv_data(char* data, 
    char* beton_amount_table_file, 
    char* beton_amount_table_with_odds_file, 
    int* wager_length, 
    char* expectId,
    float* target_amount,
    float* tolerance);

void parser_data(char* data, 
    char* beton_amount_table_file, 
    char* beton_amount_table_with_odds_file, 
    int* wager_length, 
    char* expectId,
    float* target_amount,
    float* tolerance,
    int* result_count);
#endif