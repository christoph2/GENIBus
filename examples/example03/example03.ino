#include <SPI.h>
#include <Ethernet.h>
#include <Genibus.h>

#define GB_MASTER_ADDRESS  0x01

byte macAddress[] = { 0xde, 0xad, 0xaf, 0xfe, 0xaa, 0x55  };
IPAddress subnet = (255, 255, 255, 0);
#define LOCAL_PORT  6734

/* TODO: The IP-configuration has to be adjusted to your needs!!! */
IPAddress myIP(192, 168, 100, 20);
IPAddress serverIP(192, 168, 100, 10);
IPAddress gateway = (192, 168, 100, 1);

#define LED_PIN  9  /* Pin 13 has an LED connected on most Arduino boards, otherwise this should be changed. */
                    /* Pin 9: led connected on Arduino Ethernet board*/

EthernetClient client;

void setup(void)
{
  SPI.begin();
  Ethernet.begin(macAddress, myIP);
  //server.begin();

  delay(1000); // give the Ethernet shield a second to initialize:.
  
  if (client.connect(serverIP, LOCAL_PORT)) {
  } else {
  }
  
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void frameReceived(uint8 * buffer, uint8 len)
{
  writeToServer(buffer, len);
}

GB_Datalink link(Serial, frameReceived);

void loop(void)
{
  link.connectRequest(GB_MASTER_ADDRESS);

  delay(2000);
}

void serialEvent(void)
{
   link.feed(); 
}

void writeToServer(byte const * data, byte len)
{   
    if (client.connected()) {
      client.write(data, len); 
      client.println();
    }
}

unsigned long time;
 time = millis();

