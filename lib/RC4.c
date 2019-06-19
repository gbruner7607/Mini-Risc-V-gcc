#include"imod.h"
#include"fu.h"

int main(void) {
	int S[256];
	for (int i = 0; i < 256; i++) 
		S[i] = i;
	
	int k = 0;
	int index2 = 0;
	for (int counter = 0; counter < 256; counter++) {
		index2 = imod((k + S[counter] + index2),256);
		int tmp = S[counter];
		S[counter] = S[index2];
		S[index2] = tmp;
	}
	
	fu(S[0],S[1],S[2], S[3], S[4]);	
	
	while(1);
	return 0;

}
