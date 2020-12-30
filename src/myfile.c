#include "../header/myfile.h"

void pathCombine(char* dst, const char* path1, const char* path2)
{
    if(path1 == NULL && path2 == NULL) {
        strcpy(dst, "");;
    }
    else if(path2 == NULL || strlen(path2) == 0) {
        strcpy(dst, path1);
    }
    else if(path1 == NULL || strlen(path1) == 0) {
        strcpy(dst, path2);
    } 
    else {
        char directory_separator[] = "/";
#ifdef WIN32
        directory_separator[0] = '\\';
#endif
        int len = strlen(path1);
        const int last_char = *(path1 + len -1);
        const int first_char = *path2;
        //log_debug("pathCombine: last_char=%d, first_char=%d", last_char, first_char);
        if((last_char != 47 && first_char == 47) ||
            (last_char == 47 && first_char != 47) ) {
            strcpy(dst, path1);
            strcat(dst, path2);
        }
        else if (last_char == 47 && first_char == 47)
        {
            strcpy(dst, path1);
            strcat(dst,  (char*)path2 + 1);
        }
        else if (last_char != 47 && first_char != 47)
        {
            strcpy(dst, path1);
            strcat(dst, "/");
            strcat(dst, path2);
        }
    }
}

int exists(const char* path)
{
    struct stat buffer;
    int exist = stat(path, &buffer);
    //printf("exists=%d, path= %s<====\n", exist, path);
    if(exist == 0)
        return 1;
    else // -1
        return 0;
}

int readContent(char *content, const char* path)
{
    FILE *fp;
    size_t source_size;

    fp = fopen(path, "r");
    if (!fp) {
        log_error(stderr, "Failed to load file.\n");
        exit(EXIT_FAILURE);
    }
    source_size = fread( content, 1, MAX_SOURCE_SIZE, fp);
    //printf(source_str);
    if(fp)
        fclose( fp );
    
    return source_size;
}