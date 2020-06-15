__kernel void calc_numbers_risk(__global float* settle_vector,
                                 __global float* numbers_matrix,
                                 __global float* result,
                                 int selection_length)
{

   int numbers_index = get_global_id(0);
   int numbers_size = get_global_size(0);

   float sum = 0;
   for(int i=0; i<= selection_length -1; i++)
   {
      int index = (numbers_index * 10) + i;
      //printf("numbers_index=%d, snumbers_matrix[%d]=%f, settle_vector[%d]=%f, sum=%f\n", numbers_index, index, numbers_matrix[index], i, settle_vector[i], sum);
      sum += numbers_matrix[index] * settle_vector[i];
   }
   //printf("\n");
   //printf("numbers_index=%d, numbers_size=%d, sum=%f\n", numbers_index, numbers_size, sum);
   result[numbers_index] = sum;
}