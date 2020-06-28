#include "Common.h"

/* Flag set by ‘--verbose’. */
static int verbose_flag;
static struct option long_options[] =
{
    /* These options set a flag. */
    {"version",                 no_argument,            0, 'V'},
    {"kernel-program",          required_argument,      0, 'k'},
    {"opencode-answer",         required_argument,      0, 'o'},
    {"log",                     required_argument,      0, 'l'},
    {"help",                    no_argument,            0, 'h'},
    {"beton-amount",            required_argument,      0, 'a'},
    {"beton-amount-with-odds",  required_argument,      0, 'w'},
    {"show-gpu-info",           no_argument,            0, 's'},
};

void Help()
{
    printf("option\n");
    printf("-V, -version                     Show program version.\n");
    printf("-k, --kernel-program <path>      Path to opencl kernel program.\n");
    printf("-o, --opencode-answer <path>     Path to opencode anser csv path.\n");
    printf("-l, --log <path>                 Path to program runtime log.\n");
    printf("--beton-amount <path>            Path to bet amount csv path.\n");
    printf("--beton-amount-with-odds <path>  Path to bet amount with odds csv path.\n");
    printf("-s, --show-gpu-info              Show GPU info.\n");
}

bool LoadArgs(int argc, char* argv[], 
        char kernel_program_path[], 
        char opencode_answer_path[], 
        char beton_amount_path[],
        char beton_amount_with_odds_path[],
        char log_dir[])
{
    int cmd_opt;
    cl_device_id* devices = NULL;
    cl_uint total_devices = 0;
    while(1) {
        /* getopt_long stores the option index here. */
        int option_index = 0;

        cmd_opt = getopt_long (argc, argv, "Vk:o:l:hs", /* v不用帶參數, k:必須要帶參數 a:必須要帶參數 h不用帶參數 l:必須要帶參數 */
                       long_options, &option_index);   
        /* Detect the end of the options. */
        if (cmd_opt == -1) {
            break;
        }

        switch (cmd_opt)
        {
        case 'V':
            printf("Version:%s\n", VERSION);
            return true;

        case 'k':
            strcpy(kernel_program_path, optarg);
            break;

        case 'o':
            strcpy(opencode_answer_path, optarg);
            break;

        case 'l':
            strcpy(log_dir, optarg);
            break;
        
        case 'a':
            strcpy(beton_amount_path, optarg);
            break;

        case 'w':
            strcpy(beton_amount_with_odds_path, optarg);
            break;

        case 'h':
            Help();
            return true;
        
        case 's':
            total_devices = GetDevices(&devices);
            // show device info
            for(int deviceId = 0; deviceId < total_devices; deviceId++)
            {
                printf("==================== GPU%d ====================\n", deviceId);
                show_device_information(devices[deviceId]);
                printf("==============================================\n");
            }
            if(devices)
                free(devices);
            return true;

        case '?':
            /* getopt_long already printed an error message. */
            Help();
            return true;

        default:
            abort ();
        }
    } 
    return false;
}