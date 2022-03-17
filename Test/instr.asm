while: 
        scall 0
        add r0,r1,r2
        add r0,7,r4
        seq r4,r2,r3
        braz r3,end
        branz r3, label3
end:
        add r1,1,r2
label3:
        add r1,5,r4
        jmp while, r0