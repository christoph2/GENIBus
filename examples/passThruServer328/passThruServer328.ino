#include <SPI.h>
#include <UIPEthernet.h>
#include <GB_Datalink.h>
#include <Genibus.h>

#define GB_MASTER_ADDRESS  0x01

byte macAddress[] = { 0x90, 0xa2, 0xda, 0x00, 0x69, 0x4b };
#define LOCAL_PORT  6734

/* TODO: The IP-configuration has to be adjusted to your needs!!! */
IPAddress myIP(192, 168, 1, 3);
IPAddress serverIP(192, 168, 1, 2);

int EN = 2;
int LED_PIN = 9;

EthernetServer server(LOCAL_PORT);
EthernetClient client;

void setRxMode(void);
void setTxMode(void);
void readRequest(EthernetClient tcpClient);

void setup(void)
{
    SPI.begin();
    Ethernet.begin(macAddress, myIP);
    server.begin();

    delay(1000);
    Serial.begin(9600);

    pinMode(EN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);
    setTxMode();
}

void frameReceived(uint8 * buffer, uint8 len)
{
    setTxMode();
    delay(500);
    digitalWrite(LED_PIN, LOW);

    client.write(buffer, len);
    client.stop();
}

void errorCallout(Gb_Error error, uint8 * buffer, uint8 len)
{
    setTxMode();
    delay(500);
    digitalWrite(LED_PIN, LOW);

    client.write(buffer, len);
    client.stop();
}

GB_Datalink link(Serial, frameReceived, errorCallout);

void loop(void)
{
    client = server.available();

    if (client) {
        setTxMode();
        digitalWrite(LED_PIN, HIGH);
        readRequest(client);
    }
    delay(50);
}

void serialEvent(void)
{
    link.feed();
}

void readRequest(EthernetClient tcpClient)
{
    byte totalLength = 0;
    byte remainingBytes = 0;
    char ch;

    while (tcpClient.connected()) {
        if (tcpClient.available()) {
            ch = tcpClient.read();
            link.write(ch);

            if (totalLength == 0x01) {
                remainingBytes = (byte)ch + 2;
            } else if (totalLength > 1) {
                remainingBytes -= 1;

                if (remainingBytes == 0) {
                    link.reset();
                    delay(2);
                    setRxMode();
                    return;
                }
            }
            totalLength += 1;
        }
    }
}

void setRxMode(void)
{
    digitalWrite(EN, LOW);
    digitalWrite(LED_PIN, LOW);
}

void setTxMode(void)
{
    digitalWrite(EN, HIGH);
    digitalWrite(LED_PIN, LOW);
}

