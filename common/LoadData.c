#include "Common.h"

void ReadBetonAmountFromCsv(char* beton_amount_path, cl_float** beton_amount)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_bet_amount_index = 0;

    fp = fopen(beton_amount_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", fp);
        exit(EXIT_FAILURE);
    }
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;
            
        p = NULL;
        for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
        {
            float ret = strtof(p, NULL);
            *(*beton_amount + csv_bet_amount_index) = ret;
            csv_bet_amount_index ++;
        }
    }
    fclose(fp);
}

void GetDataLength(char* opencode_answer_path, int* opencodeLength, int* betonLength)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_row_index = 0;
    int csv_column_index = 0;

    fp = fopen(opencode_answer_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", fp);
        exit(EXIT_FAILURE);
    }

    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;

        if(csv_row_index == 0){
            p = NULL;
            csv_column_index = 0;
            for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
            {
                if(csv_row_index == 0){
                    //all beton
                    if(csv_column_index >= 1)
                    {
                        (*betonLength)++;
                    }
                    csv_column_index++;
                }
            }
        }else
        {
            (*opencodeLength)++;
        }
        csv_row_index++;
    }

    fclose(fp);
    if (line)
        free(line);
}

void ReadOpnecodeAnswerFromCsv(char* opencode_answer_path, cl_int** opencode_answer, char*** opencodeList)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_column_index = 0;
    int csv_row_index = 0;
    int row_index = 0;
    long long opencode_answer_index = 0;

    fp = fopen(opencode_answer_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", fp);
        exit(EXIT_FAILURE);
    }

    char* opencode = "1-2-3-4-5-6-7-8-9-10";
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;
            
        p = NULL;
        csv_column_index = 0;
        for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
        {
            if(csv_row_index >=1){
                if(csv_column_index == 0){
                    //Load opencode list
                    *(*opencodeList + (csv_row_index -1)) = (char*) malloc(sizeof(char) * 20);
                    strcpy(*(*opencodeList + (csv_row_index -1)), p);
                    printf("opencodeList[%d] = %s \n",  (csv_row_index -1),   *(*opencodeList + (csv_row_index -1))    );
                }
                else
                {
                    int ret = strtol(p, NULL, 10);
                    *(*opencode_answer + opencode_answer_index) = ret;
                    opencode_answer_index ++;
                }
            }
            else
            {
                //all beton
                opencode = p;
                //printf("%s\n", opencode);
            }
            csv_column_index ++;
            
        }
        csv_row_index++;
    }

    fclose(fp);
    if (line)
        free(line);
}