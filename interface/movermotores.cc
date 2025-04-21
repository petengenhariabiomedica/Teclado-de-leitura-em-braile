#include <conio.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>

void traduzbraille(int lb, int lmb[])
{
  int comp,i;
  int matrizbraille[26][6] = {{1,0,0,0,0,0},{1,0,1,0,0,0},{1,1,0,0,0,0},{1,1,0,1,0,0},{1,0,0,1,0,0},{1,1,1,0,0,0},{1,1,1,1,0,0},{1,0,1,1,0,0},{0,1,0,1,0,0},{0,1,1,1,0,0},{1,0,0,0,1,0},{1,0,1,0,1,0},{1,1,0,0,1,0},{1,1,0,1,1,0},{1,0,0,1,1,0},{1,1,1,0,1,0},{1,1,1,1,1,0},{1,0,1,1,1,0},{0,1,1,0,1,0},{0,1,1,1,1,0},{1,0,0,0,1,1},{1,0,1,0,1,1},{0,1,1,1,0,1},{1,1,0,0,1,1},{1,1,0,1,1,1},{1,0,0,1,1,1}};
  comp = lb- 97;
  for (i = 0; i < 6; i++)
  {
    lmb[i] = matrizbraille[comp][i];
  }
  return ;
}

//void moverservo ()
//{
  //;
//}




int main()
{
  char letrarecebida;
  int letrabraille[6],letrabr,k;
  letrarecebida = 'a';
  letrabr = letrarecebida;
  traduzbraille(letrabr,letrabraille);
  for (k = 0; k < 6; k++)
  {
    printf("%i",letrabraille[k]);
  }
}