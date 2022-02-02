# include <stdio.h>

# define NUM_REGS 32
int regs[ NUM_REGS ];

int program[] = { 0x82000e1, 0x10600043, 0x19c00109};

/* program counter */
int pc = 0;

/* fetch the next word from the program */
int fetch()
{
  return program[ pc++ ];
}

/* instruction fields */
int instrNum = 0;
int reg1     = 0;
int reg2     = 0;
int reg3     = 0;
int imm      = 0;

/* decode a word */
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
      regs[ reg3 ] = regs[ reg1 ] -  reg2 ;
      }
      else{
        printf( "sub r%d,r%d,r%d\n", reg1, reg2, reg3 );
        regs[ reg3 ] = regs[ reg1 ] + regs[ reg2 ];
      }
      break;
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
