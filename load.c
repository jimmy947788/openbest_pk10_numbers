#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/types.h>
#include "header/mytype.h"

int read_beton_length(char* opencode_answer_path)
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
    char* opencode_pointer = NULL;

    timeStart = clock();
    fp = fopen(opencode_answer_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", (long)fp);
        exit(EXIT_FAILURE);
    }
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;
        if (csv_row_index == 0)
        {
              printf("%s\n",line);
            p = NULL;
            csv_column_index = 0;
            //printf("%s\n", line);
            for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
            {
                csv_column_index ++;   
            }
        }
        if  (csv_row_index >0)
            break;

        csv_row_index++;
    }

    fclose(fp);
    if (line)
        free(line);

    timeEnd = clock();
    return csv_column_index -1;
}

int load_opnecode_answer_table(char* opencode_answer_path, char*** opencode_list, _Bool** opencode_answer_table)
{
    char OPENCODE_SAMPLE[] = "1-2-3-4-5" ;
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
    int opencode_length = strlen(OPENCODE_SAMPLE);
    char* opencode_pointer = NULL;

    timeStart = clock();
    fp = fopen(opencode_answer_path, "r");
    if (fp == NULL){
        printf("read file failed: %ld\n", (long)fp);
        exit(EXIT_FAILURE);
    }
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(len <= 0)
            break;
        printf("==========>csv_row_index[%d], ", csv_row_index );
        if (csv_row_index >0) //header不要
        {
            p = NULL;
            csv_column_index = 0;
            //printf("length=%d\n", strlen(line) );
            //printf("line=%s\n",line );
            for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
            {
                //printf("csv_column_index=%d,", csv_column_index);
                //printf("p=%s\n", p);
                if(csv_column_index == 0){
                    // Load opencode list 
                    // 把csv檔案的第1欄opencode存到opencode_list
                    *(*opencode_list + (csv_row_index-1)) = (char*) malloc(sizeof(char) * opencode_length);
                    strcpy(*(*opencode_list + (csv_row_index-1)), p);
                    //printf("opencode_list[%d] = %s \n", opencodeList  );
                }
                else
                {
                    // 把csv檔案第1欄後面的答案存到opencode_answer
                    //short ret = strtol(p, NULL, 10);
                    // miuns 45, plus 43 
                    if(strcmp(p, "-1") == 0)
                        *(*opencode_answer_table + opencode_answer_index) = 45; //-
                    else
                        *(*opencode_answer_table + opencode_answer_index) = 43;//+
                    //printf("%d,",  *(*opencode_answer_table + opencode_answer_index) );
                    opencode_answer_index ++;
                }
                csv_column_index ++;
                
            }
            printf("csv_column length=%d\n",  csv_column_index );
        }
        csv_row_index++;
    }

    fclose(fp);
    if (line)
        free(line);

    timeEnd = clock();
    return csv_row_index - 1; //header不要
}

int main(int argc, char const *argv[])
{
    char OPENCODE_SAMPLE[] = "1-2-3-4-5" ;
    char *opencode_answer_path = "data/opencode_ssc_table_1.csv";

    int beton_length = read_beton_length(opencode_answer_path);

    /*
    int opencode_length = 100000;
    char* opencode_answer_table;
    char** opencodeList;
    opencode_answer_table = (char *)malloc(sizeof(char) * (opencode_length / 2) * beton_length);
    opencodeList = (char**)malloc(sizeof(*opencodeList) * (opencode_length / 2));
    int ret = load_opnecode_answer_table(opencode_answer_path, &opencodeList, &opencode_answer_table); 

    printf("beton_length:%d\n",beton_length);
    printf("opnecode_answer_table length:%d\n", ret);
    printf("opencodeList[0]=%s\n", opencodeList[0]);
    printf("opencodeList[1]=%s\n", opencodeList[1]);
    printf("opencodeList[2]=%s\n", opencodeList[2]);

    printf("opencodeList[49997]=%s\n", opencodeList[49997]);
    printf("opencodeList[49998]=%s\n", opencodeList[49998]);
    printf("opencodeList[49999]=%s\n", opencodeList[49999]);
    printf("opencodeList[50000]=%s\n", opencodeList[50000]);

    char in;
    scanf("%c",&in);
    /* code */
    return 0;
}
