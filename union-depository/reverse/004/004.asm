global _start:

section .data:
    pass times 50 db 0
    string1 db "Enter password: "
    string2 db "Correct", 10
    string3 db "Wrong", 10

section .text:
_start:
    mov rsi, string1
    mov rbx, 16
    call print_str
    mov rax, 0
    mov rdi, 0
    mov rsi, pass
    mov rdx, 50
    syscall
    call check_palindrome
    call check_len
    mov rsi, string2
    mov rbx, 8
    jmp finish
    not_correct_pass:
    mov rsi,string3
    mov rbx,6
    finish:
    call print_str
    mov rax, 60
    mov rdi, 0
    syscall


check_palindrome:
    mov rdi, pass
    run1:
      cmp byte[rdi], 10
      je end_run1
      inc rdi
      jmp run1

    end_run1:
    dec rdi
    mov rsi, pass

    run2:
      cmp rdi, rsi
      jle end_run2
      mov al, [rdi]
      mov ah, [rsi]
      cmp al, ah
      jne not_correct_pass
      dec rdi
      inc rsi
      jmp run2

    end_run2:
    ret

check_len:
      mov rdi, pass
      mov rbx, 0
      run3:
        cmp byte [rdi],10
        je end_run3
        inc rdi
        inc rbx
        jmp run3
      end_run3:
      cmp rbx,4
      jl not_correct_pass
      ret

print_str:
    mov rax, 1
    mov rdi, 1
    mov rdx, rbx
    syscall
    ret

