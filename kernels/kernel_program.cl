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
    __global const uchar *answers_matrix, 
    __global float *result,
    const uint beton_length) {

  size_t numbers_index = get_global_id(0);
  size_t numbers_size = get_global_size(0);
  //printf("numbers_index=%d, numbers_size=%d, beton_length=%d\n", numbers_index, numbers_size, beton_length);
  
  uint step = beton_length;
  ulong index = 0; //5883099999;
  //printf("numbers_index=%d, answers_matrix[0]=%d, answers_matrix[%lu]=%d\n", numbers_index, answers_matrix[0], index, answers_matrix[index]);
  //printf("total_amount_vector[%d]=%f, total_amount_odds_vector[%d]=%f\n", 
  //  beton_length-1, total_amount_vector[beton_length-1], 
  //  beton_length-1, total_amount_odds_vector[beton_length-1]);

  float sum = 0;
  for (int i = 0; i <= beton_length - 1; i++) {
    index = (numbers_index * step) + i; 　//千萬不要動！！　只要有任何轉型或優先調整都會跑掉
    /*
    //debug 用
    if(index >= 5883099990)
      printf("numbers_index=%d, answers_matrix[%lu]=%d\n", 
        numbers_index, index, answers_matrix[index]);
    */
    /*
    //debug 用
    if( total_amount_odds_vector[i] > 0 ||  total_amount_vector[i] > 0)
      printf("total_amount_odds_vector[%d]=%f,  total_amount_vector[%d]=%f\n", 
        i, total_amount_odds_vector[i],
        i, total_amount_vector[i]);
  */
    if (answers_matrix[index] == 43)// +1
    {
      result[numbers_index] += total_amount_odds_vector[i]; //有中獎就用乘上賠率的金額
      //sum+= total_amount_odds_vector[i]; //有中獎就用乘上賠率的金額
    }
    else if (answers_matrix[index] == 44) // 0
    {
      result[numbers_index] += 0; // 和 (不算輸贏)
    }
    else if (answers_matrix[index] == 45) // -1
    {
      result[numbers_index] += total_amount_vector[i] * -1; //沒中獎就用本金
      //sum += total_amount_vector[i] * -1; //沒中獎就用本金
    }
    //printf("answers_matrix[%lu]=%d, sum=%f\n",  index,  answers_matrix[index],  sum);
  }

  //printf("\n");
  //printf("numbers_index=%d, numbers_size=%d, result[%d]=%f\n", numbers_index, numbers_size,  numbers_index, result[numbers_index]);
  
  //debug用 
  //result[numbers_index] = numbers_index; 
  //result[numbers_index] = sum;
}