
static uint8 sendBuffer[0xff];
static Crc crc(0xffffu);

static const uint8 connectReqPayload[] = {
  0x00, 0x02, 0x02, 0x03, 0x04, 0x02, 0x2e, 0x2f, 0x02, 0x02, 0x94, 0x95
};

void dumpPDU(byte len)
{
  uint8 idx;

  for (idx = 0; idx < (len + 6); ++idx) {
     //printf("%#x ", sendBuffer[idx]);   
     sendBuffer[idx];
  }
}

void connectRequest(uint8 sa)
{
   sendPDU(0x27, 0xfe, sa, connectReqPayload, ARRAY_SIZE(connectReqPayload)); 
}

void sendPDU(uint8 sd, uint8 da, uint8 sa, uint8 const * data, uint8 len)
{
  uint8 idx;
  uint16 calculatedCrc;

  sendBuffer[0] = sd;
  sendBuffer[1] = len + ((uint8)0x02);
  sendBuffer[2] = da;
  sendBuffer[3] = sa;
  
  for (idx = ((uint8)0x00); idx < len; ++idx) {
    sendBuffer[idx + ((uint8)0x04)] = data[idx];
  }

  crc.init(0xffff);
  for (idx = ((uint8)0x01); idx < (len + ((uint8)0x04)); ++idx) {
    crc.update(sendBuffer[idx]);
  }
  calculatedCrc = crc.get();
  sendBuffer[idx] = HIBYTE(calculatedCrc);
  sendBuffer[idx + 1] = LOBYTE(calculatedCrc);  
  
  for (idx = 0; idx < (len + ((uint8)0x06)); ++idx) {
     Serial.write(sendBuffer[idx]);
  }
}

