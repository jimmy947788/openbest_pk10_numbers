__kernel void sum_selection_total_amount(__global float* settle_vector,
                                 __global float* wager_matrix,
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
         //printf("wager_matrix[%d]=%f, ", index, wager_matrix[index]);
      }
      //printf("\n");
      result[col_index] = settle_vector[col_index] * sum;
   }
   else
   {
      result[col_index] = 0;
   }
}