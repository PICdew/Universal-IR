unsigned char EDGE=1;
void INT_Init(){
  INTCON.INTF=0;
  INTCON.INTE=1;
  OPTION_REG.INTEDG=1;
}

void main() {
  UART1_Init(57600);               // Initialize UART module at 57600bps
  Delay_ms(100);                  // Wait for UART module to stabilize
  TRISB=0b00000001;
  INT_Init();                     //Initialize RB0 interrupt
  INTCON.GIE=1;         //Interrupt is enabled
  while(1){
     UART1_Write(EDGE);
  }
}                // end of main
void interrupt(){
  INTCON.GIE=0;
  INTCON.INTF=0;
  EDGE=1-EDGE;
  OPTION_REG.INTEDG=EDGE;
  INTCON.GIE=1;
}
