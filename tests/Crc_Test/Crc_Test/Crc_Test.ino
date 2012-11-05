
#include <Genibus.h>

/*
**
**  Known-good telegrams and CRCs.
**
*/
uint8 TestVector0[] = {
    0x27, 0x07, 0x20, 0x01, 0x02, 0xC3, 0x02, 0x10, 0x1A
};

uint8 TestVector1[] = {
    0x27, 0x0e, 0xfe, 0x01, 0x00, 0x02, 0x02, 0x03, 0x04, 0x02, 0x2e, 0x2f, 0x02, 0x02, 0x94, 0x95
};

uint8 TestVector2[] = {
  0x24, 0x0e, 0x01, 0x20, 0x00, 0x02, 0x46, 0x0e, 0x04, 0x02, 0x20, 0xf7, 0x02, 0x02, 0x03, 0x01
};

uint8 TestVector3[] = {
  0x24, 0x10, 0x01, 0x20, 0x02, 0x0c, 0x82, 0x3e, 0x00, 0x39, 0x82, 0x15, 0x00, 0x64, 0x82, 0x09, 0x00, 0xfa
};

uint8 TestVector4[] = {
  0x27, 0x0f, 0x20, 0x01, 0x02, 0x04, 0x02, 0x10, 0x1a, 0x1b, 0x04, 0x02, 0x04, 0x05, 0x03, 0x81, 0x06
};

uint8 TestVector5[] = {
  0x24, 0x0e, 0x01, 0x20, 0x02, 0x04, 0x7a, 0x42, 0x39, 0x80, 0x04, 0x02, 0xb5, 0xc8, 0x03, 0x00
};

uint16 ExpectedResults[] = {
  0x901c,
  0xa2aa,
  0x0004,
  0x910a,
  0x802a,
  0xf2d7
};

/*
**  Calculate the CRC of a GENIBus telegram (excluding start-delimiter).
*/
uint16 calculateCRC(uint8 const * array, uint16 len)
{
  uint16 idx;
  
  Crc_Init(0xffffu);
  for (idx = (uint16)1u; idx < len; ++idx) {
    Crc_Update(array[idx]);
  }
  return Crc_Get();
}

void resultOK(uint16 value, uint16 expected)
{
   if (value == expected) {
      Serial.println("OK");
   } else {
      Serial.println("Invalid CRC!!!");
   } 
}

void setup(void)
{
  Serial.begin(9600); 
}

void loop(void)
{
   uint16 result;
   
   result = calculateCRC(TestVector0, ARRAY_SIZE(TestVector0));
   resultOK(result, ExpectedResults[0]);
   
   result = calculateCRC(TestVector1, ARRAY_SIZE(TestVector1));
   resultOK(result, ExpectedResults[1]);
   
   result = calculateCRC(TestVector2, ARRAY_SIZE(TestVector2));
   resultOK(result, ExpectedResults[2]);
   
   result = calculateCRC(TestVector3, ARRAY_SIZE(TestVector3));
   resultOK(result, ExpectedResults[3]);   
   
   result = calculateCRC(TestVector4, ARRAY_SIZE(TestVector4));
   resultOK(result, ExpectedResults[4]); 
   
   result = calculateCRC(TestVector5, ARRAY_SIZE(TestVector5));
   resultOK(result, ExpectedResults[5]);    
}


