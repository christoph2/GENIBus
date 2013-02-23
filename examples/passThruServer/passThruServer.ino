#include <SPI.h>
#include <Ethernet.h>
#include <Genibus.h>

#define GB_MASTER_ADDRESS  0x01

byte macAddress[] = { 0x90, 0xa2, 0xda, 0x00, 0x69, 0x4b  };

IPAddress subnet = (255, 255, 255, 0);
#define LOCAL_PORT  6734

/* TODO: The IP-configuration has to be adjusted to your needs!!! */
IPAddress myIP(192, 168, 1, 3);        // for Linux users: adjust the two first line on the file /etc/hosts:
IPAddress serverIP(192, 168, 1, 2);    // IP address of "localhost" must be the same as "IPAddress serverIP", for example "192.168.1.2  localhost"
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

    //Serial.print("Frame completed!");
    //Serial.print("\n\r");

    // TAP#4 - If we reach this point, TestClient should be able to receive an display the completed frame.
    client.write(buffer, len);
    client.stop();
}

void errorCallout(Gb_Error error, uint8 * buffer, uint8 len)  //  Needs latest software version to compile!!!
{
    //Serial.print("CRC-Error\n\r"); // Only a single cause of error right now.
    client.write(buffer, len);
    client.stop();
}

GB_Datalink link(Serial, frameReceived, errorCallout);

byte header[4];
byte apdus[0xff];

void loop(void)
{
    client = server.available();

    if (client) {

        //Serial.print(" server available ");
        //Serial.print("\n\r");
        //delay(500);

        // TAP#1 - Indicates basic TCP/IP connectivity.
        readRequest(client);
    }
    delay(50);
}


void serialEvent(void)
{
    //Serial.print(" OK 1 ");
    //Serial.print("\n\r");
    //delay(500);

    // TAP#3 - Pump received a correct request and is now answering.
    link.feed();
}


void writeToClient(EthernetClient client, byte const * data, byte len)
{
    client.write(data, len);
    client.stop();
    //Serial.print(" OK 2 ");
    //Serial.print("\n\r");
    //delay(500);
}

void readRequest(EthernetClient client)
{
    byte totalLength = 0;
    byte remainingBytes;
    char ch;

    while (client.connected()) {
        if (client.available()) {
            ch = client.read();
            //link.write(ch);

            //Serial.print("ch: ");
            //Serial.print(ch);
            //Serial.print(" OK 3 ");
            //Serial.print("\n\r");

            if (totalLength == 0x01) {  // Length byte.
                remainingBytes = (byte)ch + 2;

                //Serial.print(" OK 4 ");
                //Serial.print("\n\r");

            } else if (totalLength > 1) {
                remainingBytes -= 1;

                //Serial.print(" OK 5 ");
                //Serial.print("\n\r");

                if (remainingBytes == 0) {

                    //Serial.print("TCP frame completed");
                    //Serial.print("\n\r");
                    link.reset();
                    // TAP#2 - Complete telegram received from TestClient.
                    return;
                }
            }
            totalLength += 1;

            //Serial.print(" OK 7 ");
            //Serial.print("\n\r");

        }
    }
}

