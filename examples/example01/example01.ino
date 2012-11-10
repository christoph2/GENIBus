#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Genibus.h>

byte macAddress[] = { 0xde, 0xad, 0xaf, 0xfe, 0xaa, 0x55  };
byte ipAddress[] = {192, 168, 100, 20};
IPAddress ip(192, 168, 1, 177);
byte gateway[] = { 192, 168, 100, 1 };
byte subnet[] = { 255, 255, 255, 0 };
unsigned int localPort = 6734;

void setup(void)
{
  Serial.begin(9600);
  Ethernet.begin(macAddress, ipAddress);
  
  delay(1000); 
}

void loop(void)
{

  while (true) {
    /* Endless loop. */
  }
}

