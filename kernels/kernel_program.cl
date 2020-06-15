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

__kernel void sum_selection_total_amount(
                                 __global const float* settle_vector,
                                 __global const float* wager_matrix,
                                 __global float* result,
                                 int row_size )
{

   int col_index = get_global_id(0);
   int col_size = get_global_size(0);

   int bit = (int)settle_vector[col_index];
   //printf("settle_vector[%d]=%d\n", col_index, bit);
   if(bit > 0)
   {
      float sum = 0;
      for(int i=0; i<= row_size -1; i++)
      {
         int index = (i * col_size ) + col_index; 
         sum += wager_matrix[index];
         //printf("wager_matrix[%d]=%f, \n", index, wager_matrix[index]);
      }
      //printf("\n");
      result[col_index] = settle_vector[col_index] * sum;
     // printf("result[%d]=%f, \n", col_index, result[col_index]);
   }
   else
   {
      result[col_index] = 0;
   }
}