#include <iostream>
#include <wiringPi.h>
using namespace std;

int main()
{
    if (wiringPiSetupGpio() == -1) {
        std::cout << "Erro wiringpi" << std::endl;
        return 1;
    }

    int testPin = 13;

    pinMode(testPin, INPUT);

    int t = 0;

    while (true)
    {

    t = digitalRead(testPin);

    cout << t << endl;

    delay(2000);
    }
}