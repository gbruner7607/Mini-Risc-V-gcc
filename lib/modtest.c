#include"imod.h"
#include"fu.h"

int main(void) {
	int a = 16;
	int b = 3;
	int c = imod(a,b);
	fu(a,b,c);
	while(1);
	return 0;
}
