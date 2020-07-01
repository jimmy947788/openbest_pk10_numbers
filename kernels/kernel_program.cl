__kernel void sum_beton_total_amount(
         __global const ushort* mask,
         __global const float* amount,
         __global float* result,
         const int row_size)
{

   int col_index = get_global_id(0);
   int col_size = get_global_size(0);

   int bit = mask[col_index];
   //printf("mask[%d]=%d\n", col_index, bit);
   if(bit > 0)
   {
      float sum = 0;
      for(int i=0; i<= row_size -1; i++)
      {
         int index = (i * col_size ) + col_index; 
         sum += amount[index];
         //printf("amount[%d]=%f, \n", index, amount[index]);
      }
      //printf("\n");
      result[col_index] = mask[col_index] * sum;
      //printf("result[%d]=%f, \n", col_index, result[col_index]);
   }
   else
   {
      result[col_index] = 0;
   }
}

__kernel void calc_numbers_risk(
         __global const float* total_amount_vector,      /* 各beton加總陣列（本金）*/
         __global const float* total_amount_odds_vector, /* 各beton加總陣列（本金*賠率 - 本金）*/
         __global const short* answers_matrix,
         __global float* result,
         const int beton_length)
{

   int numbers_index = get_global_id(0);
   int numbers_size = get_global_size(0);

   float sum = 0;
   float total_amount = 0;
   float total_amount_odds = 0;
   int step = beton_length;
   for(int i=0; i<= beton_length -1; i++)
   {
      int index = (numbers_index * step) + i; 
      total_amount = total_amount_vector[i];
      total_amount_odds = total_amount_odds_vector[i];
      if(answers_matrix[index]>0)
         sum += total_amount_odds; //有中獎就用乘上賠率的金額
      else
         sum += total_amount * -1; //沒中獎就用本金
      //printf("answers_matrix[%d]=%f, total_amount=%f, total_amount_odds=%f, sum=%f\n", index, answers_matrix[index], total_amount, total_amount_odds, sum);
   }
   //printf("\n");
   //printf("numbers_index=%d, numbers_size=%d, sum=%f\n", numbers_index, numbers_size, sum);
   result[numbers_index] = sum;
}