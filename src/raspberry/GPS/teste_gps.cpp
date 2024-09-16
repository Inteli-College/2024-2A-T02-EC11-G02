#include <iostream>
#include <wiringPi.h>
#include <wiringSerial.h>

int main() {
    int serial_port;
    if ((serial_port = serialOpen("/dev/ttyS0", 9600)) < 0) {
        std::cerr << "Erro ao abrir a porta serial!" << std::endl;
        return 1;
    }
    wiringPiSetup();
    while (true) {
        if (serialDataAvail(serial_port)) {
            char c = serialGetchar(serial_port);
            std::cout << c; // Imprime o caractere recebido
        }
    }
    serialClose(serial_port);
    return 0;
}