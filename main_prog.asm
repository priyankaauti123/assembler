section .data
    a db "hello",10,0
    c dd 10
	b dd 10
	pf db "Enter ur r no"
	arr dd 0,3,5,2,00
section .bss
	a1 resd 1
	a2 resb 10
section .text
	global main
	extern printf

main:
	mov eax , ebp
	mov ebx , eax
	mov eax , ebx
	mov eax , ecx
	mov eax , [arr]
	mov eax , 10
	mov ax , [b]
	mov eax , edx
	mov ebx , esi
	mov ecx , [a]
	mov ecx , [pf]
	mov ecx , [a1]
	mov bx , bx
