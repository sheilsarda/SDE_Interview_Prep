#include <stdint.h>
#include <stdio.h>
#include <cstring>

#define DISPLAY_MESSAGE 0x34
#define MOTOR_MESSAGE 0x80


// Handle Display messages
void display_message(uint8_t *m, uint16_t message_len){

    for(int i = 0; i < message_len; ++i)
      printf("%c ", m[i]);

    printf("\r\n");
}

// Handle Motor messages
void update_motor(float forward_back, float left_right){

  printf("Forward Back   %f \r\n", forward_back);
  printf("Left Right     %f \r\n", left_right);

}

void dispatcher(uint8_t *packet){
  
  uint8_t  packet_id    = packet[0];
  uint8_t  message_type = packet[1];
  uint16_t message_len  = packet[2] || (packet[3] << sizeof(uint8_t));


  printf("============================\r\n");
  printf("Packet ID      %d \r\n", packet_id);

  if(message_type == DISPLAY_MESSAGE){
    uint8_t message[message_len];
    for(int i = 0; i < message_len; ++i)
      message[i] = packet[4 + i];

    printf("Type           DISPLAY \r\n");
    printf("Length         %d \r\n", message_len);

    display_message(message, message_len);

  } else {
    printf("Type           MOTOR \r\n");

    uint32_t forward_back = 0x0;
    uint32_t left_right   = 0x0;
    
    for(int i = 0; i < 4; ++i){
      forward_back |= (packet[4 + i] << (8 * sizeof(uint8_t) * i));
      left_right   |= (packet[8 + i] << (8 * sizeof(uint8_t) * i));
    }

    float fb_float, lr_float;

    memcpy(&fb_float, &forward_back, sizeof(float));
    memcpy(&lr_float, &left_right,    sizeof(float));
    
    update_motor(fb_float, lr_float); 
    
  }
}


int main(){

  uint8_t display_packet[] = {0x1, 0x34, 0x05, 0x0, 0x48, 0x65, 0x6c, 0x6c, 0x6f};
  uint8_t motor_packet[] = {0x2, 0x80, 0x08, 0x0, 0x0, 0x0, 0x80, 0x3f, 0x0, 0x0, 0x0, 0xbf};

  dispatcher(display_packet);
  dispatcher(motor_packet);
  
  return 0;
}
