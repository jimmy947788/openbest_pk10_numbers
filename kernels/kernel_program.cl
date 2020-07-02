#pragma OPENCL EXTENSION cl_khr_global_int32_base_atomics : enable
#define LOCK(a) atomic_cmpxchg(a, 0, 1)
#define UNLOCK(a) atomic_xchg(a, 0)

__kernel void sum_beton_total_amount(
         __global const ushort* mask,
         __global const float* amount,
         __global float* result,
         const int row_size)
{

   int col_index = get_global_id(0);
   int col_size = get_global_size(0);

   ushort bit = mask[col_index];
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

__kernel void find_best_amount_count(
         __global float* amount_array,
         __global uint* count_result,
         const float amount_range1,
         const float amount_range2)
{

   int numbers_index = get_global_id(0);
   int numbers_size = get_global_size(0);
   float amount = amount_array[numbers_index];

   if(amount_range1 <=amount && amount <=amount_range2 )
   {
      //printf("amount_array[%d]=%f\n", numbers_index, amount_array[numbers_index]);
      atomic_inc(count_result);
   }
}

__kernel void find_best_amount(
         __global float* amount_array,
         __global int* best_amount_count,
         __global uint* result_array,
         __global int* mutex,
         const float amount_range1,
         const float amount_range2)
{

   int numbers_index = get_global_id(0);
   int numbers_size = get_global_size(0);
   float amount = amount_array[numbers_index];

   while(LOCK(mutex));
   int gindex = *best_amount_count;
   if(gindex < 3250 && amount_range1 <=amount && amount <=amount_range2 )
   {
      printf("amount_array[%d]=%f\n", numbers_index, amount_array[numbers_index]);
      printf("best_amount_count=%d\n", gindex);
      result_array[gindex] = numbers_index;
      *best_amount_count +=1;
      
   }
   UNLOCK(mutex);
}