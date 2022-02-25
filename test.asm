label1:
    add r3,20,r4
label2:
    add r3,50,r4
label3:
    add r3,100,r4
Else:
    add r3,0,r4
end: stop

label4:
    seq r1,1,r2
    branz r2,label1
    seq r1,2,r2
    branz r2, label2
    seq r1,3,r2
    branz r2, label3
    jmp r2, r0

;=========================================

;Exo2
add r1,1,r2
add r3,0,r4

while:
    seq r2,128,r5
    branz r5,label2
    mul r2,2,r2
    add r4,1,r4
    jmp label1, r0


;====================


label1:
    slt r1,200,r3
    

    add r3,1,r3


;======================== 21/02/2022 ==================================

main:
    jmp simple, r1

simple:
    jmp r1, r0




