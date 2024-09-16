#include <iostream>
#include <wiringPi.h>
#include <wiringSerial.h>
#include <string>

using namespace std;

void processGPSData(string data);
string convertToDegrees(const string& raw_value, char direction);

int main() {
    int serial_port;

    // Inicializa a biblioteca WiringPi
    if (wiringPiSetupGpio() == -1) {
        cerr << "Erro ao inicializar o WiringPi!" << endl;
        return 1;
    }

    // Configuração da UART nos pinos GPIO 14 e 15
    pinMode(14, HIGH);  // Configura GPIO 14 como TXD (função alternativa 0)
    pinMode(15, HIGH);  // Configura GPIO 15 como RXD (função alternativa 0)

    // Abre a porta serial
    if ((serial_port = serialOpen("/dev/ttyAMA10", 9600)) < 0) {
        cerr << "Erro ao abrir a porta serial!" << endl;
        return 1;
    }

    // String para armazenar os dados do GPS
    string gps_data = "";

    while (true) {
        // Verifica se há dados disponíveis na serial
        cerr << "Entrou no while" << endl;
        cout << serialDataAvail(serial_port) << endl;
        while (serialDataAvail(serial_port)) {
            char c = serialGetchar(serial_port);
            cout << c;
            if (c == '\n') { // Quando uma sentença NMEA completa é recebida
                if (gps_data.find("$GPGGA") != string::npos) {
                    processGPSData(gps_data);
                }
                gps_data = ""; // Limpa a string para a próxima sentença
            } else {
                gps_data += c; // Concatena os caracteres na string
            }
        }
        delay(1000); // Aguarda 1 segundo antes de ler novamente
    }

    serialClose(serial_port); // Fecha a porta serial
    return 0;
}

void processGPSData(string data) {
    string latitude, longitude, date;
    size_t start = 0, end = 0;
    int field = 0;

    // Itera sobre os campos da sentença NMEA
    while ((end = data.find(",", start)) != string::npos) {
        string token = data.substr(start, end - start);
        start = end + 1;
        field++;

        if (field == 3) {
            latitude = convertToDegrees(token, data[start]);
        }
        if (field == 5) {
            longitude = convertToDegrees(token, data[start]);
        }
        if (field == 10) {
            date = data.substr(start, 6);  // Assume que o campo 10 tem a data
        }
    }

    cout << "Latitude: " << latitude << endl;
    cout << "Longitude: " << longitude << endl;
    cout << "Data: " << date << endl;
}

string convertToDegrees(const string& raw_value, char direction) {
    if (raw_value.empty()) return "";

    double degrees = stod(raw_value.substr(0, 2));
    double minutes = stod(raw_value.substr(2));
    double result = degrees + minutes / 60.0;

    if (direction == 'S' || direction == 'W') {
        result = -result;
    }

    return to_string(result);
}
