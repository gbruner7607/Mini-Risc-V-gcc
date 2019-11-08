#ifndef LFSRH
#define LFSRH

// int __prx__;
// int __a__;
// int __c__;
// int __m__;

// void randInit(int seed, int a, int c, int m); 
// int rand(); 

unsigned int __lfsr_state;

void seed_lfsr(unsigned int seed);
unsigned int lfsr();

#endif
