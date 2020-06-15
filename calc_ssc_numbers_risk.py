import pyopencl as cl
import numpy as np
import itertools
import time

if __name__ == "__main__":

    # Create context and command queue
    platform = cl.get_platforms()[0]
    devices = platform.get_devices()
    context = cl.Context(devices)
    queue = cl.CommandQueue(context)

    # Open program file and build
    program_text = ""
    with open('kernels/calc_numbers_risk.cl', 'r') as program_file: # Scale x Matrx
        program_text = program_file.read()
    program = cl.Program(context, program_text)

    try:
        program.build()
    except:
        print("Build log:")
        print(program.get_build_info(devices[0],
                cl.program_build_info.LOG))
        raise

    all_balls = list(itertools.product([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], repeat=5))
    selection_length = 2359
    numbers_length = len(all_balls)
    print("selection size=", selection_length, ", numbers=",  numbers_length)
    # Create arguments for kernel: a scalar, a LocalMemory object, and a buffer
    selection = np.random.randint(0, 1500, size=selection_length).astype(np.float32)
    print("selection=", selection)
    print("selection=", selection.shape)

    numbers = np.random.randint(2, size=(selection_length * numbers_length)).astype(np.float32)
    print("numbers=", numbers)
    print("numbers=", numbers.shape)

    result = np.empty(numbers_length, dtype=np.float32)

    tStart = time.time()#計時開始
    # create buffer READ/WRITE  cl.mem_flags.READ_WRITE
    buffer_selection = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=selection)
    buffer_numbers = cl.Buffer(context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=numbers)
    buffer_result = cl.Buffer(context, cl.mem_flags.READ_WRITE,  result.nbytes)

    # Create, configure, and execute kernel (Seems too easy, doesn't it?)
    global_work_offset = (0, )
    global_work_size = (numbers_length, )
    local_work_size = (1, )
    kernel = program.calc_numbers_risk
    kernel.set_arg(0, buffer_selection)
    kernel.set_arg(1, buffer_numbers)
    kernel.set_arg(2, buffer_result)
    kernel.set_arg(3, np.int32(selection_length))

    ev = cl.enqueue_nd_range_kernel(queue, kernel, global_work_size, local_work_size, global_work_offset)

    # Read data back from buffer
    result = np.empty(numbers_length, dtype=np.float32)
    cl.enqueue_copy(queue, result, buffer_result)
    print("result=", result)
    #cl.enqueue_copy(queue, buffer_result, result)

    tEnd = time.time()#計時結束
    print("It cost %f sec" % (tEnd - tStart))#會自動做近位

    #print("result length:", len(result))
    #print("result=", result)