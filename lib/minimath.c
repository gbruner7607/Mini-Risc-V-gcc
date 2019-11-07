#include"minimath.h"

int __mulsi3(int a, int b) {
	int i;
	int c = 0;
   	for (i = 0; i < b; i++) c += a; 
	return c;
}

int __modsi3(int a, int b) {
	int c = a;
	while((c - b) >= 0)
		c = c - b; 
	return c; 
} 

int __divsi3(int a, int b) {
	int c = 0; 
	while(a > 0) {
		a = a - b; 
		if (a >= 0) c++; 
	}
	return c; 
}
