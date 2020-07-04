#include "Common.h"

void load_beton_amount_table(char* beton_amount_path, cl_float** beton_amount_table)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_bet_amount_index = 0;
    clock_t timeStart, timeEnd;
    
    timeStart = clock();
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
            *(*beton_amount_table + csv_bet_amount_index) = ret;
            csv_bet_amount_index ++;
        }
    }
    if (line)
        free(line);
    fclose(fp);

    timeEnd = clock();
    printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
}

void get_opnecode_answer_table_shape(char* opencode_answer_path, int* betonLength, uint32* opencodeLength)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_row_index = 0;
    int csv_column_index = 0;
    clock_t timeStart, timeEnd;

    timeStart = clock();
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
    if (line)
        free(line);
    fclose(fp);

    timeEnd = clock();
    printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
}

void load_opnecode_answer_table(char* opencode_answer_path, cl_short** opencode_answer, char*** opencodeList)
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    int csv_column_index = 0;
    int csv_row_index = 0;
    uint32 opencode_answer_index = 0;
    clock_t timeStart, timeEnd;

    timeStart = clock();
    fp = fopen(opencode_answer_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", fp);
        exit(EXIT_FAILURE);
    }
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
                    //printf("opencodeList[%d] = %s \n",  (csv_row_index -1),   *(*opencodeList + (csv_row_index -1))    );
                }
                else
                {
                    short ret = strtol(p, NULL, 10);
                    *(*opencode_answer + opencode_answer_index) = ret;
                    opencode_answer_index ++;
                }
            }
            else
            {
                //all beton
                //printf("%s\n", p);
            }
            csv_column_index ++;
            
        }
        csv_row_index++;
    }

    fclose(fp);
    if (line)
        free(line);

    timeEnd = clock();
    printf("execution \033[1;37m%s\033[0m time:\033[1;36m%f\033[0ms\n", __FUNCTION__, (double)(timeEnd - timeStart) / CLOCKS_PER_SEC);
}