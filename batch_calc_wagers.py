import numpy as np
import pyopencl as cl
import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

if __name__ == "__main__":
    platfrom = cl.get_platforms()[0] #礦雞要用1
    devices = platfrom.get_devices(cl.device_type.GPU)
    context = cl.Context(devices)

    queue = cl.CommandQueue(context, devices[0], cl.command_queue_properties.PROFILING_ENABLE)
    dev_name = queue.get_info(cl.command_queue_info.DEVICE).get_info(cl.device_info.NAME)
    print("Devices: %s" % dev_name)

    program_file = open("kernel_program.cl", "r")
    program_text = program_file.read()
    program_file.close()

    program = cl.Program(context, program_text)

    try:
        program.build(devices=devices)
    except:
        print("build log")
        print(program.get_build_info(devices[0], cl.program_build_info.LOG)) 
        raise


    a = np.array([
        [1, 0, 1]
    ])
    b = np.random.randint(10, size=(3, 3))
    print(a)
    print(b)
    print("===============================================")
    #c = np.zeros(3, 3)

    # Create buffers
    mf = cl.mem_flags
    buffer_a = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    buffer_b = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b) 
    buffer_c = cl.Buffer(context, mf.WRITE_ONLY, a.nbytes)
    #buffer_width = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, 3) 

    # Set buffers as arguments to the kernel
    # The arguments can also be specified by calling kernel(....) directly instead
    kernel = program.matrix_mul 
    kernel.set_arg(0, buffer_a)
    kernel.set_arg(1, buffer_b)
    kernel.set_arg(2, buffer_c)

    #mult_kernel = program.multiply
    #print("Kernel Name:")
    #print(mult_kernel.get_info(cl.kernel_info.FUNCTION_NAME))
    #program_file.close()

    #program.vecadd(queue, a.shape, None, a_b, a_b, c_g)

    # Enqueue kernel (with arguments)
    n_globals = b.shape
    n_locals = None
    cl.enqueue_nd_range_kernel(queue, kernel, n_globals, n_locals)


    # Enqueue command to copy from buffer one to buffer two
    a_plus_b = np.empty_like(a)
    cl.enqueue_read_buffer(queue, buffer_c, a_plus_b).wait()

    print(a_plus_b)