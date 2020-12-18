#pragma OPENCL EXTENSION cl_khr_global_int32_base_atomics : enable
#define LOCK(a) atomic_cmpxchg(a, 0, 1)
#define UNLOCK(a) atomic_xchg(a, 0)

__kernel void sum_beton_total_amount(
      __global const ushort *mask,
      __global const float *amount,
      __global float *result,
      const int row_size) 
      {

  int col_index = get_global_id(0);
  int col_size = get_global_size(0);

  ushort bit = mask[col_index];
  // printf("mask[%d]=%d\n", col_index, bit);
  if (bit > 0) {
    float sum = 0;
    for (int i = 0; i <= row_size - 1; i++) {
      int index = (i * col_size) + col_index;
      sum += amount[index];
      //printf("amount[%d]=%f, \n", index, amount[index]);
    }
    // printf("\n");
    result[col_index] = mask[col_index] * sum;
    // printf("result[%d]=%f, \n", col_index, result[col_index]);
  } else {
    result[col_index] = 0;
  }
}

__kernel void calc_numbers_risk(
    __global const float *total_amount_vector, /* 各beton加總陣列（本金）*/
    __global const float *total_amount_odds_vector, /* 各beton加總陣列（本金*賠率 - 本金）*/
    __global const char *answers_matrix, 
    __global float *result,
    const int beton_length) {

  int numbers_index = get_global_id(0);
  int numbers_size = get_global_size(0);
  //printf("numbers_index=%d, numbers_size=%d, beton_length=%d\n", numbers_index, numbers_size, beton_length);
  
  int step = beton_length;
  unsigned int index = 0;
  for (int i = 0; i <= beton_length - 1; i++) {
    index = (numbers_index * step) + i;
    // miuns 45, plus 43
    int sign = (int)answers_matrix[index];
    /*
    if(total_amount_odds_vector[i] > 0)
      printf("total_amount_odds_vector[%d]=%f\n", i, total_amount_odds_vector[i]);
    
    if(total_amount_vector[i] > 0)
      printf("total_amount_vector[%d]=%f\n", i, total_amount_vector[i]);
    */
    if (sign== 43)
    {
      result[numbers_index] += total_amount_odds_vector[i]; //有中獎就用乘上賠率的金額
    }
    else
    {
      result[numbers_index] += total_amount_vector[i] * -1; //沒中獎就用本金
    }
    //printf("answers_matrix[%d]=%d, total_amount=%f, total_amount_odds=%f,sum=%f\n", 
    //  index, answers_matrix[index], total_amount, total_amount_odds, sum);
  }

  //printf("\n");
  //printf("numbers_index=%d, numbers_size=%d, sum=%f\n", numbers_index, numbers_size,  result[numbers_index]);
  
  //debug用 
  //result[numbers_index] = numbers_index; 
}