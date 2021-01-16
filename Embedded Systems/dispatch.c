#define DISPLAY_MESSAGE 0x34
#define MOTOR_MESSAGE 0x80


// Handle Display messages
int display_message(uint8_t *m, uint16_t message_len){

  return 1;
}

// Handle Motor messages
int update_motor(float forward_back, float left_right){

  return 1;
}

int dispatcher(uint8_t packet){
  
  uint8_t  packet_id      = packet[0];
  uint8_t  message_type   = packet[1];
  uint16_t message_length = packet[2] || (packet[3] << sizeof(uint8_t));

  uint8_t message_data[message_length];

  return 0;
}
