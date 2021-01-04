
#include "../header/mystring.h"

int count(const char str[], char c)
{
    //計算element數量
    int length = 0;
    for(int i = 0; str[i] != '\0'; i++)
    {
        if(str[i] == c)
            ++length;
    }
    //printf("===================>length=%d\n",length);
    return length;
}

int split(char* list[], const char str[], const char delim[])
{
    size_t len = 0;
    char *p = NULL;
    int index = 0;
    //寫入element to list
    p = NULL;
    for(p = strtok(str, delim); p != NULL; p = strtok(NULL, delim))
    {
        //printf("%s, len:%d\n", p, strlen(p));
        list[index] = (char*)malloc(sizeof(char) * (strlen(p) + 1));
        memset(list[index], '\0', sizeof(char) * (strlen(p) + 1));
        strcpy(list[index],  p); 
        //printf("%s, len:%d\n",  list[index], strlen( list[index]));
        index ++;
    }
    return index; 
}

int contains(const char str[], const  char* list[], int len)
{
    int ret = -1;
    char* tmp;
    for(int i =0; i<= len-1; i++)
    {
        //log_debug("str=%s, len=%d", str, strlen(str));
        //log_debug("lsit[%d]=%s,  len=%d", i, list[i], strlen(list[i]));
        if(strcmp(str, list[i]) ==0){
            //log_debug("=============>find %s in list", str);
            return 1;
        }
    }
    return ret;
}

char* substring(const char s_src[], int i_start, int i_end)
{
    char * p_stmp;
    int substrlength = i_end - i_start ;
    printf ("==========>Malloc size:%i\n", substrlength);
    log_debug("substring before : %s", s_src);
    p_stmp = (char *) malloc(sizeof(char) * (substrlength + 2)); //+1會有後面亂碼的問題
    memset(p_stmp, '\0', sizeof(char) * (substrlength + 2));
    strncpy(p_stmp, s_src + i_start, substrlength);
    log_debug("substring after : %s", s_src);
    return p_stmp;
}