//#include<stdio.h>
#include"fu.h"

int main(void) {
	int s[10];
	for (int i = 0; i < 10; i++) {
		s[i] = (i);
	}
	int a = s[3];
	int b = s[4];
	int c = s[5];
	int d = s[6];
	int e = s[7];
	fu(a,b,c,d,e);
	while(1);
	return 0;
}
