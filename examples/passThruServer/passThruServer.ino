#include <SPI.h>
#include <Ethernet.h>
#include <Genibus.h>

#define GB_MASTER_ADDRESS  0x01

byte macAddress[] = { 0xde, 0xad, 0xaf, 0xfe, 0xaa, 0x55  };
IPAddress subnet = (255, 255, 255, 0);
#define LOCAL_PORT  6734

/* TODO: The IP-configuration has to be adjusted to your needs!!! */
IPAddress myIP(192, 168, 1, 3);        // for Linux users: adjust the two first line on the file /etc/hosts:
IPAddress serverIP(192, 168, 1, 2);    // IP address of "localhost" must be the same as "IPAddress serverIP", for example "192.168.1.2	localhost" 
//IPAddress gateway = (192,168, 1, 1);    // and, 2nd line, "192.168.1.2   'my computer name'" 

#define LED_PIN  9  /* Pin 13 has an LED connected on most Arduino boards, otherwise this should be changed. */
                    /* Pin 9: led connected on Arduino Ethernet board*/

EthernetServer server(LOCAL_PORT);
EthernetClient client;
boolean alreadyConnected = false;

void setup(void)
{
  SPI.begin();
  Ethernet.begin(macAddress, myIP);
  server.begin();
  
  delay(1000); // give the Ethernet shield a second to initialize:.

  Serial.begin(9600);
   
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void frameReceived(uint8 * buffer, uint8 len)
{
  // TAP#4 - If we reach this point, TestClient should be able to receive an display the completed frame.
  client.write(buffer, len);
}

GB_Datalink link(Serial, frameReceived);

byte header[4];
byte apdus[0xff];

void loop(void)
{
  client = server.available();

  if (client) {
    // TAP#1 - Indicates basic TCP/IP connectivity.
    readRequest(client);
  }
  delay(50);
}


void serialEvent(void)
{
   // TAP#3 - Pump received a correct request and is now answering.
   link.feed(); 
}


void writeToClient(EthernetClient client, byte const * data, byte len)
{   
  client.write(data, len); 
}

void readRequest(EthernetClient client)
{
  byte totalLength = 0;
  byte remainingBytes;
  char ch;
  
  while (client.connected()) {
      if (client.available()) {
        ch = client.read();
        link.write(ch);
        if (totalLength == 0x01) {  // Length byte.
          remainingBytes = (byte)ch + 2;
        } else if (totalLength > 1) {
          remainingBytes -= 1;
          if (remainingBytes == 0) {
            // TAP#2 - Complete telegram received from TestClient.
            client.stop();
            return;
          }
        }     
        totalLength += 1;
      }
  }
}

