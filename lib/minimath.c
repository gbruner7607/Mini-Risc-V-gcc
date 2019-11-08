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

int expo(int a, int b) {
	int result = 1;

	while(b) {
		if (b&1) {
			result *= a;
		}
		b >>=1;
		a *= a; 
	}

	return result;
}

int modexpo(int a, uint n, int p) {
	int res = 1; 
	a = a % p; 

	while (n > 0) {
		if (n & 1) res = (res * a) % p; 

		n = n >> 1; 
		a = (a*a) % p; 
	}
	return res; 
}

int gcd(int a, int b) {
	if (a < b) return gcd(b, a); 
	else if (a%b == 0) return b;
	else return gcd(b, a%b); 
}