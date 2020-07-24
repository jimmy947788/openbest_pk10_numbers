#include "../header/argument.h"

/* Flag set by ‘--verbose’. */
static int verbose_flag;
static struct option long_options[] =
{
    /* These options set a flag. */
    {"version",                             no_argument,               0, 'V'},
    {"kernel-program",               required_argument,      0, 'k'},
    {"opencode-answer-table",  required_argument,      0, 'o'},
    {"log",                                   required_argument,      0, 'l'},
    {"help",                                 no_argument,                0, 'h'},
    {"show-gpu-info",                no_argument,                0, 's'},
};

void help()
{
    printf("option\n");
    printf("-V, -version                                               Show program version.\n");
    printf("-k, --kernel-program <path>                   Path to opencl kernel program.\n");
    printf("-o, --opencode-answer-table <path>      Path to opencl kernel program.\n");
    printf("-l, --log <path>                                        Path to program runtime log.\n");
    printf("-s, --show-gpu-info                                  Show GPU info.\n");
}

void laod_args(int argc, char* argv[], 
        char kernel_program_path[], 
        char*** opencode_answer_table_path, 
        char log_dir[])
{
    int cmd_opt;
    cl_platform_id* platforms = NULL;
    cl_uint total_platforms = 0;
    cl_device_id* devices = NULL;
    cl_uint total_devices = 0;
    //char** opencode_answer_table_path;

    // for split ','
    //======================
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    char delim[] = ",";
    char *p = NULL;
    //======================

    while(1) {
        /* getopt_long stores the option index here. */
        int option_index = 0;

        cmd_opt = getopt_long (argc, argv, "Vk:l:hs", /* v不用帶參數, k:必須要帶參數 a:必須要帶參數 h不用帶參數 l:必須要帶參數 */
                       long_options, &option_index);   
        /* Detect the end of the options. */
        if (cmd_opt == -1) {
            break;
        }

        switch (cmd_opt)
        {
        case 'V':
            printf("Version:%s\n", VERSION);
            exit(EXIT_SUCCESS);

        case 'k':
            strcpy(kernel_program_path, optarg);
            break;

        case 'l':
            strcpy(log_dir, optarg);
            break;
            
        case 'h':
            help();
            exit(EXIT_SUCCESS);
        
        case 's':
            total_platforms = get_platforms(&platforms);
            total_devices = create_gpu_device_list(platforms[0], &devices);
            // show device info
            for(int deviceId = 0; deviceId < total_devices; deviceId++)
            {
                printf("==================== GPU%d ====================\n", deviceId);
                show_device_information(devices[deviceId]);
                printf("==============================================\n");
            }
            if(devices)
                free(devices);
            exit(EXIT_SUCCESS);

        case 'o':
            //printf("optarg=%s\n", optarg);
            *opencode_answer_table_path = (char**)malloc(sizeof(**opencode_answer_table_path) * 2);
            //split read opencode_answer_table_path1
            p = strtok(optarg, delim);
            *(*opencode_answer_table_path + 0) = (char*) malloc(sizeof(char) * MAX_LENGTH);
            memset( *(*opencode_answer_table_path + 0) , '\0', MAX_LENGTH);
            strcpy(*(*opencode_answer_table_path + 0), p);
            //printf("opencode_answer_table_path[0]=%s\n", *(*opencode_answer_table_path + 0));

           //split read opencode_answer_table_path2
            p = strtok(NULL, delim);
            *(*opencode_answer_table_path + 1) = (char*) malloc(sizeof(char) * MAX_LENGTH);
              memset( *(*opencode_answer_table_path + 1) , '\0', MAX_LENGTH);
            strcpy(*(*opencode_answer_table_path + 1), p);
            //printf("opencode_answer_table_path[1]=%s\n", *(*opencode_answer_table_path + 1));
            break;
        case '?':
            /* getopt_long already printed an error message. */
            help();
            exit(EXIT_SUCCESS);

        default:
            abort ();
        }
    } 
}