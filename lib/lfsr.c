#include"lfsr.h"
//#include"minimath.h" 

// void randInit(int seed, int a, int c, int m) {
// 	__prx__ = seed; 
// 	__a__ = a; 
// 	__c__ = c;
// 	__m__ = m;
// }

// int rand() {
// 	__prx__ = ((__a__ * __prx__) + __c__) % __m__; 
// 	return __prx__;
// }

// unsigned short lfsr(unsigned short state) {
// 	unsigned short bit; 
// 	bit = ((state >> 0) ^ (state >> 2) ^ (state >> 3) ^ (state >> 5)); 
// 	state = (state >> 1) | (bit << 15); 
// 	return state; 
// }

void seed_lfsr(unsigned int seed) {
	__lfsr_state = seed;
}

unsigned int lfsr() {
	unsigned int state = __lfsr_state;
	unsigned int bit; 
	bit = ((state >> 0) ^ (state >> 1) ^ (state >> 2) ^ (state >> 22) );//^ (state >> 31)); 
	state = (state >> 1) | (bit << 31);
	__lfsr_state = state;
	return state;
}