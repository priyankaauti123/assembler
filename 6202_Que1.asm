	%include"6202_Q1_macro.mac"
section .data
	str1 db "hello",0,10
	pf db "no of vowel:=%d",10,0
	str2 db "aeiou",0
	len1 equ $-str2

section .bss
	n1 resd 1
	n2 resd 1
	str3 resb 30

section .text
	global main
	extern printf

main:
	mov ebx,str1
	mov edx,str2
	vowel_count ebx,edx
	mov ecx,edx
	
