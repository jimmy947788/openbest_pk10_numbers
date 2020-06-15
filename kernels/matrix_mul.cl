__kernel void matrix_mul(__global float *A, __global float *B, __global float *C) {
    
    // Get the index of the current element
    int size = get_global_size(0);
    int i = get_global_id(0);
    int j = get_global_id(1);

    float acc = 0;

    if (i < size && j < size) {
    	for (int k=0; k<size; k++)
        {
    		//acc += A[j*size + k] * B[i*size + k];
	    	acc += A[j*size + k] * B[k*size + i];
        }
	    C[j*size + i] = acc;
        //printf("get_global_size(0)=%d, get_global_size(1)=%d\n", get_global_size(0), get_global_size(1));
	}
}
