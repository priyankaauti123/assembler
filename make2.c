#include<stdio.h>
#include<stdlib.h>
int main()
 {
   int n1;
    printf("Enter file no 1:=assembler or 2:=macro_assembler ");
    scanf("%d",&n1);
    if(n1==1)
    {
      system("python assembler.py");
    }
    if(n1==2)
    {
      system("python macro_assembler.py");
    }
 }




