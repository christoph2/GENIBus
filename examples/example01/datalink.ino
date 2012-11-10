
static uint8 sendBuffer[0xff];
static Crc crc(0xffffu);

uint16 sendPDU(uint8 sd, uint8 da, uint8 sa, uint8 * data, uint8 len)
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
  

#if 0
  res = ReadCOMPort(data, 256, &uNumRead);

  if (res != S_OK) {
    GetFormattedError(res, msg, 1024);
    return ERR_WINDOWS;
  } 
  else {
    if (uNumRead == 0) {
      return ERR_TIMEOUT;
    }

    if ((CheckCRC(data, uNumRead)) == TRUE) {
      if (data[0] == SD_DATA_REPLY) {
        if (source_address == data[2]) {
          len = data[1];

          if (destination_address == ADDR_CONNECT_REQU) {
            connect_addr = data[3]; /* Connect-Request. */
          }

          idx    = 4;
          ao_i   = 0; /* ADPUs_out_idx. */

          while (idx < len + 1) {
            adpu_len   = (data[idx + 1] & 0x3f);
            adpu_class = data[idx];

            for (i = 0; i < numpdus_in; i++) {    /* Prüfen, ob die ADPU angefordert wurde. */
              if ((HIBYTE(adpus_in[i].adpu_head)) == adpu_class) {
                adpus_out[ao_i].adpu_head = MAKEWORD(data[idx], data[idx + 1]);

                if (adpu_class == CLASS_ASCII_STRINGS) {
                  strncpy((char *)adpus_out[ao_i].adpu_data,
                  (char *)&data[idx + 2], MAX_ASCII_LEN / 2);
                } 
                else if (adpu_class == CLASS_COMMANDS) {
                } 
                else {
                  if (adpu_len > 0) {             /* Daten entsprechend der Länge kopieren. */
                    uint8 t;
                    t = MIN(adpu_len, LOBYTE(   /* schützt vor Buffer-Overflows. */
                    adpus_out[ao_i].adpu_head));
                    memcpy((void *)adpus_out[ao_i].adpu_data, (void *)&data[idx + 2], t);
                  }
                }

                break;
              }
            }

            idx += (adpu_len + 2);
          }
        } 
        else {
          return ERR_WRONG_ADDR;
        }
      } 
      else {
        return ERR_FRAMING;
      }
    } 
    else {
      return ERR_CRC;
    }
  }
#endif
  //Sleep(50);
}

