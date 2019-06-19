#include"imod.h"

int imod(int a, int b) {
	int c = a; 
	while((c - b) >= 0)
		c = c - b; 
	return c;
}
