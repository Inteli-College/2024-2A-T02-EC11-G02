#include <iostream>
#include <wiringPi.h>
using namespace std;

int main()
{
    if (wiringPiSetupGpio() == -1) {
        std::cout << "Erro wiringpi" << std::endl;
        return 1;
    }

    int ledPin = 26;

    pinMode(ledPin, OUTPUT);

    std::cout << "Ligando" << std::endl;
    digitalWrite(ledPin, HIGH);

    delay(3000);

    std::cout << "Desligando" << std::endl;
    digitalWrite(ledPin, LOW);

    return 0;
}