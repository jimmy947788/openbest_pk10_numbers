/*
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
*/

__kernel void beton_total_amount(
         __global const float* one_vector_mask,
         __global const float* amount_matrix,
         __global float* result,
         const int row_size)
{

   int col_index = get_global_id(0);
   int col_size = get_global_size(0);

   int bit = (int)one_vector_mask[col_index];
   //printf("one_vector_mask[%d]=%d\n", col_index, bit);
   if(bit > 0)
   {
      float sum = 0;
      for(int i=0; i<= row_size -1; i++)
      {
         int index = (i * col_size ) + col_index; 
         sum += amount_matrix[index];
         //printf("amount_matrix[%d]=%f, \n", index, amount_matrix[index]);
      }
      //printf("\n");
      result[col_index] = one_vector_mask[col_index] * sum;
      //printf("result[%d]=%f, \n", col_index, result[col_index]);
   }
   else
   {
      result[col_index] = 0;
   }
}

__kernel void calc_numbers_risk(
         __global const float* total_amount_vector,
         __global const float* total_amount_odds_vector,
         __global const float* answers_matrix,
         __global float* result,
         const int beton_length)
{

   int numbers_index = get_global_id(0);
   int numbers_size = get_global_size(0);

   float sum = 0;
   float total_amount = 0;
   float total_amount_odds = 0;
   for(int i=0; i<= beton_length -1; i++)
   {
      int index = (numbers_index * 10) + i;
      total_amount = total_amount_vector[i];
      total_amount_odds = total_amount_odds_vector[i];
      if(answers_matrix[index]>0)
         sum += total_amount_odds;
      else
         sum += total_amount * -1;
      //printf("answers_matrix[%d]=%f, total_amount=%f, total_amount_odds=%f, sum=%f\n", index, answers_matrix[index], total_amount, total_amount_odds, sum);
   }
   //printf("\n");
   //printf("numbers_index=%d, numbers_size=%d, sum=%f\n", numbers_index, numbers_size, sum);
   result[numbers_index] = sum;
}