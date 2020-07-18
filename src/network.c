#include "../header/network.h"

int create_socket()
{
    int sockfd = 0, ret = 0;
    sockfd = socket(AF_INET , SOCK_STREAM , 0);
    if (sockfd == -1){
        printf("Fail to create a socket.");
        exit(EXIT_FAILURE); 
    }
    //socket的連線
    struct sockaddr_in serverInfo;
    bzero(&serverInfo,sizeof(serverInfo));

    serverInfo.sin_family = PF_INET;
    serverInfo.sin_addr.s_addr = INADDR_ANY;
    serverInfo.sin_port = htons(SOCKET_PORT);
    ret = bind(sockfd,(struct sockaddr *)&serverInfo,sizeof(serverInfo));
    if(ret == -1)
    {
        printf("bind error. (%d)", ret);
        exit(EXIT_FAILURE); 
    }
    ret = listen(sockfd, 5);
    if(ret == -1)
    {
        printf("listen error. (%d)", ret);
        exit(EXIT_FAILURE); 
    }
    return sockfd;
}

void parser_data(char* data, 
    char* beton_amount_table_file, 
    char* beton_amount_table_with_odds_file, 
    int* wager_length, 
    char* expectId,
    float* target_amount,
    float* tolerance)
{
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;

    //split read beton_amount_table_file
    p = strtok(data, delim);
    memset(beton_amount_table_file, '\0', MAX_LENGTH);
    strcpy(beton_amount_table_file, p);
    //split read beton_amount_table_with_odds_file
    p = strtok(NULL, delim);
    memset(beton_amount_table_with_odds_file, '\0', MAX_LENGTH);
    strcpy(beton_amount_table_with_odds_file, p);
    //split read wager_length
    p = strtok(NULL, delim);
    (*wager_length) = strtol(p, NULL, 10);
    //split read expectId
    p = strtok(NULL, delim);
    memset(expectId, '\0', MAX_LENGTH);
    strcpy(expectId, p);
    //split read target_amount
    p = strtok(NULL, delim);
    (*target_amount) = strtof(p, NULL);
    //split read tolerance
    p = strtok(NULL, delim);
    (*tolerance) = strtof(p, NULL);
}
