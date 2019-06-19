#include "imul.h"

int imul(int a, int b) {
	if ((a == 0) || (b == 0))
		return 0;
	int c = 0;
	for (int i = 0; i < b; i++) 
		c = c + a;
	return c;
}
