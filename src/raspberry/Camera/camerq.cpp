#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>
#include <zip.h>
#include <curl/curl.h>
#include <fstream>

namespace fs = std::filesystem;

bool zip_folder(const std::string& folder_path, const std::string& zip_path) {
    int err = 0;
    zip_t* zip = zip_open(zip_path.c_str(), ZIP_CREATE | ZIP_TRUNCATE, &err);

    if (!zip) {
        std::cerr << "Erro ao criar o arquivo ZIP: " << zip_path << std::endl;
        return false;
    }

    for (const auto& entry : fs::recursive_directory_iterator(folder_path)) {
        if (fs::is_directory(entry.path())) continue;

        std::string relative_path = fs::relative(entry.path(), folder_path).string();
        zip_source_t* source = zip_source_file(zip, entry.path().c_str(), 0, 0);

        if (source == nullptr || zip_file_add(zip, relative_path.c_str(), source, ZIP_FL_OVERWRITE | ZIP_FL_ENC_UTF_8) < 0) {
            std::cerr << "Erro ao adicionar o arquivo ao ZIP: " << entry.path() << std::endl;
            zip_source_free(source);
            zip_close(zip);
            return false;
        }
    }

    zip_close(zip);
    return true;
}

bool upload_zip(const std::string& zip_path, const std::string& url) {
    CURL* curl;
    CURLcode res;
    curl_mime* form = nullptr;
    curl_mimepart* field = nullptr;
    curl = curl_easy_init();

    if (curl) {
        form = curl_mime_init(curl);

        // Adiciona o arquivo ZIP ao formulário
        field = curl_mime_addpart(form);
        curl_mime_name(field, "file");
        curl_mime_filedata(field, zip_path.c_str());

        // Configura a URL de destino
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        // Configura o formulário como o corpo da requisição
        curl_easy_setopt(curl, CURLOPT_MIMEPOST, form);

        // Executa a requisição
        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            std::cerr << "Erro ao enviar o arquivo: " << curl_easy_strerror(res) << std::endl;
            curl_mime_free(form);
            curl_easy_cleanup(curl);
            return false;
        }

        // Limpeza
        curl_mime_free(form);
        curl_easy_cleanup(curl);
        return true;
    }

    return false;
}

int main(int argc, char** argv) {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open camera" << std::endl;
        return -1;
    }

    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
    cv::Mat frame;
    int frameCount = 0;

    std::string folder_name = "imagens";
    if (!fs::exists(folder_name)) {
        fs::create_directory(folder_name);
    }

    while (true) {
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "Error: Empty frame captured" << std::endl;
            break;
        }
        cv::imshow("Camera", frame);

        if (cv::waitKey(1) == 's') {
            std::string filename = folder_name + "/image_" + std::to_string(frameCount++) + ".jpg";
            cv::imwrite(filename, frame);
            std::cerr << filename + " salvo com sucesso! " << std::endl;
        }

        if (cv::waitKey(1) == 'q') {
            std::cerr << "Saindo..." << std::endl;
            break;
        }
    }

    cap.release();
    cv::destroyAllWindows();

    // Cria o arquivo ZIP a partir da pasta "imagens"
    std::string zip_path = "imagens.zip";
    if (zip_folder(folder_name, zip_path)) {
        std::cout << "Pasta compactada com sucesso: " << zip_path << std::endl;

        // Envia o arquivo ZIP para o endpoint
        std::string url = "http://10.128.0.83:8000/upload_and_process/";
        if (upload_zip(zip_path, url)) {
            std::cout << "Arquivo enviado com sucesso para " << url << std::endl;
        } else {
            std::cerr << "Falha ao enviar o arquivo!" << std::endl;
        }
    } else {
        std::cerr << "Falha ao compactar a pasta!" << std::endl;
    }

    return 0;
}