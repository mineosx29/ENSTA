#include <stdio.h>
#include <math.h>

# define NUM_REGS 32
int regs[ NUM_REGS ];
int memory[1024];

int program[] = { 0x08600043, 0x110000a6, 0x19e00109};

/* program counter */
int pc = 0;

/* fetch the next word from the program */
int fetch()
{
  return program[ pc++ ];
  // Boucle permettant de lire le fichier en sortie d'assemblage
}

/* instruction fields */
int instrNum = 0;
int reg1     = 0;
int reg2     = 0;
int reg3     = 0;
int imm      = 0;

/* decode a word */
void lire_fichier(char* fichier)
{
  char* lecture;

  FILE *fichier_read = fopen(fichier, "r");
  fscanf(fichier_read, "%s\n", &lecture);
  fclose(fichier_read);

}
void decode( int instr )
{
  instrNum = (instr & 0xF8000000) >> 27;
  reg1     = (instr & 0x7C00000 ) >>  22;
  reg2     = (instr & 0xFE0) >> 5;
  reg3     = (instr & 0x1F);
  imm      = (instr & 0x200000) >> 21;
}

/* the VM runs until this flag becomes 0 */
int running = 1;

/* evaluate the last decoded instruction */
void eval()
{
  switch( instrNum )
  {
    case 0:
      /* halt */
      printf( "halt\n" );
      running = 0;
      break;
    case 1:
      if(imm)
      {
        printf( "add r%d,%d,r%d\n",reg1, reg2, reg3 );
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1; 
        }
        regs[ reg3 ] = regs[ reg1 ] +  reg2 ;
      }
      else{
        printf( "add r%d,r%d,r%d\n",reg1, reg2, reg3 );
        regs[ reg3 ] = regs[ reg1 ] + regs[ reg2 ];
      }
      
      break;
    case 2:
      if(imm)
      {
      printf( "sub r%d,%d,r%d\n", reg1, reg2, reg3 );
      if (reg2 < 0)
      {
        reg2 = reg2 & (int) (pow(2, 16)) - 1;
      }
      regs[ reg3 ] = regs[ reg1 ] -  reg2 ;
      }
      else{
        printf( "sub r%d,r%d,r%d\n", reg1, reg2, reg3 );
        regs[ reg3 ] = regs[ reg1 ] + regs[ reg2 ];
      }
      break;
    case 3:
      if(imm)
      {
        printf("mul r%d,%d,r%d\n", reg1, reg2, reg3);
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1;        
        }
        regs[ reg3] = regs[reg1] * reg2;
      }
      else{
        printf("mul r%d,r%d,r%d\n", reg1, reg2, reg3);
        regs[ reg3] = regs[reg1] * regs[reg2];
      }
      break;
    case 4:
      if(imm)
      {
        printf("div r%d,%d;r%d\n", reg1, reg2, reg3);
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1; 
        }
        regs[ reg3] = regs[reg1] / reg2;

      }
      else
      {
        printf("div r%d, r%d,r%d\n", reg1, reg2, reg3);
        regs[reg3] = regs[reg1] /regs[reg2];
      }
      break;
    case 5:
      if(imm)
      {
        printf("and r%d, %d, r%d\n", reg1, reg2, reg3);
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1; 
        }
        regs[reg3] = regs[reg1] & reg2;
      }
      else
      {
        printf("and r%d, r%d, r%d\n", reg1, reg2, reg3);
        regs[reg3] = regs[reg1] & regs[reg2];
      }
      break;
    case 6:
      if(imm)
      {
        printf("or r%d, %d;,r%d\n", reg1, reg2, reg3);
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1; 
        }
        regs[reg3] = regs[reg1] || reg2;
      }
      else
      {
        printf("or r%d, r%d,r%d\n", reg1, reg2, reg3);
        regs[reg3] = regs[reg1] || regs[reg2];
      }
      break;
    case 7:
      if(imm)
      {
        printf("xor r%d, %d, r%d\n", reg1, reg2, reg3);
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1; 
        }
        regs[reg3] = regs[reg1] ^ reg2;
      }
      else
      {
        printf("xor r%d, r%d, r%d\n", reg1, reg2, reg3);
        regs[reg3] = regs[reg1] ^ regs[reg2];
      }
      break;
    case 8:
      if(imm)
      {
        printf("shl r%d, %d; r%d\n", reg1, reg2, reg3);
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1; 
        }
        regs[reg3] = regs[reg1] >> reg2;
      }
      else
      {
        printf("shl r%d, r%d; r%d\n", reg1, reg2, reg3);
        regs[reg3] = regs[reg1] >> regs[reg2];
      }
      break;
    case 9:
      if(imm)
      {
        printf("seq r%d, %d, r%d\n", reg1, reg2, reg3);
        if (reg2 < 0)
        {
          reg2 = reg2 & (int) (pow(2, 16)) - 1; 
        }
        if(regs[reg1] == reg2)
        {
          regs[reg3] = 1;
        }
        else
        {
           regs[reg3] = 0;

        }
      }
      else
      {
        printf("seq r%d, r%d, r%d\n", reg1, reg2, reg3);
        if(regs[reg1] == regs[reg2])
        {
          regs[reg3] = 1;
        }
        else
        {
           regs[reg3] = 0;

        }
      }
      break;
      case 10:

        if(imm)
        {
          printf("load r%d, r%d, r%d\n", reg1, reg2, reg3);
          if (reg2 < 0)
          {
            reg2 = reg2 & (int) (pow(2, 16)) - 1; 
          }
          regs[reg3] = memory[regs[reg1] + reg2];
        }
        else
        {
          printf("load r%d, r%d, r%d\n", reg1, reg2, reg3);
          regs[reg3] = memory[regs[reg1] + regs[reg2]];

        }
        break;
      case 11:
        if(imm)
        {

        }
        

  }
}

/* display all registers as 4-digit hexadecimal words */
void showRegs()
{
  int i;
  printf( "regs = " );
  for( i=0; i<NUM_REGS; i++ )
    printf( "%04X ", regs[ i ] );
  printf( "\n" );
}

void run()
{
  while( running )
  {
    showRegs();
    int instr = fetch();
    decode( instr );
    eval();
  }
  showRegs();
}



int main( int argc, const char * argv[] )
{
  run();
  return 0;
}
