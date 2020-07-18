#include "../header/loadData.h"

int readFileContent(const char* path, char *content)
{
    FILE *fp;
    size_t source_size;

    fp = fopen(path, "r");
    if (!fp) {
        fprintf(stderr, "Failed to load file.\n");
        exit(EXIT_FAILURE);
    }
    source_size = fread( content, 1, MAX_SOURCE_SIZE, fp);
    //printf(source_str);
    if(fp)
        fclose( fp );
    
    return source_size;
}

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
        printf("read file failed: %ld\n", (long)fp);
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
        printf("read file failed: %ld\n", (long)fp);
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


int load_opnecode_answer_table(char* opencode_answer_path, char*** opencode_list, cl_short** opencode_answer_table)
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
            
        p = NULL;
        csv_column_index = 0;
        for(p = strtok(line, delim); p != NULL; p = strtok(NULL, delim))
        {
            if(csv_column_index == 0){
                // Load opencode list 
                // 把csv檔案的第1欄opencode存到opencode_list
                *(*opencode_list + (csv_row_index)) = (char*) malloc(sizeof(char) * opencode_length);
                strcpy(*(*opencode_list + (csv_row_index)), p);
                //printf("opencode_list[%d] = %s \n",  (csv_row_index -1), *(*opencode_list + (csv_row_index -1))    );
            }
            else
            {
                // 把csv檔案第1欄後面的答案存到opencode_answer
                short ret = strtol(p, NULL, 10);
                *(*opencode_answer_table + opencode_answer_index) = ret;
                opencode_answer_index ++;
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
    return csv_row_index;
}