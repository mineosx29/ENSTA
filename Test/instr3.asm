label2:

    add r0, 42,r1   ;   42 in R1
    add r0,-42,r2   ;  -22 in R2
    sub r1, r2,r3   ;   20 in R3
    mul r2, r3,r1   ; -440 in R1
    jmp label1, r0

label1:
    add r0,1,r1
    stop