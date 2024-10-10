import Select from "react-select";
import { useState, useRef } from "react";
import ReportComponent from "../../../components/Report";
import { servicesVersion } from "typescript";

const options = [
  { value: "brasil-sudeste", label: "Brasil - Sudeste" },
  { value: "brasil-sul", label: "Brasil - Sul" },
  { value: "brasil-nordeste", label: "Brasil - Nordeste" },
  { value: "brasil-norte", label: "Brasil - Norte" },
  { value: "brasil-centro-oeste", label: "Brasil - Centro-Oeste" },
];

const modelVersion = [
  { value: "v1", label: "v1" },
];

export default function UploadPage() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null); 
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [dataServer, setdataServer] = useState<DataServer>({
    colorize_processed_image_url: "",
    counted: 0,
    processed_image_url: "",
    version: "",
  });
  const [processedComplete, setProcessedComplete] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false); // Loading state

  const reportSectionRef = useRef<HTMLDivElement>(null);

  interface DataServer {
    colorize_processed_image_url: string;
    counted: number;
    processed_image_url: string;
    version: string;
  }


  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files === null ){
      return;
    }

    const file = e.target.files[0];

    if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
      setSelectedImage(file);
      setProcessedImage(URL.createObjectURL(file)); // Pré-visualização da imagem
    } else {
      alert('Por favor, selecione um arquivo de imagem válido (PNG ou JPEG)');
    }
  };

  const handleSubmit = async () => {
    if (!selectedImage) {
      alert('Por favor, selecione uma imagem primeiro.');
      return;
    }

    setIsLoading(true); // Inicia o loading
    setProcessedComplete(false); 

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await fetch('/api/firebase_url', {
        method: 'POST',
        body: formData,
      });
      // colorize_processed_image_url
      // : 
      // "https://storage.googleapis.com/grupo2-93568.appspot.com/processed/tmp7jrti7ef.png"
      // counted
      // : 
      // 404
      // processed_image_url
      // : 
      // "https://storage.googleapis.com/grupo2-93568.appspot.com/processed/tmp_ykotxu4.png"
      // version
      // : 
      // "v1"
      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setdataServer(data); 
        setProcessedImage(data.processed_image_url); // URL da imagem processada pelo servidor
        setProcessedComplete(true);
      } else {
        alert('Falha no upload da imagem.');
      }
    } catch (error) {
      console.error('Erro ao fazer upload da imagem:', error);
    } finally {
      setIsLoading(false); // Finaliza o loading
      // Rolar até a seção do relatório assim que a imagem for processada
      if (reportSectionRef.current) {
        reportSectionRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <div>
      <main className="flex flex-col my-14 px-14 py-8 gap-y-10 items-center">
        <div className="w-1/2">
          <h1 className="font-bold text-[#575EA6]">Teste de modelo</h1>
          <p>
            O ESG é uma das tendências mais relevantes de mercado dos últimos tempos.
          </p>
        </div>
        <div className="flex flex-col w-1/2">
          <div className="flex flex-col gap-y-10">
            <form>
              <div>
                <div className="flex gap-x-11">
                  <div className="w-1/3">
                    <label className="font-bold">Escolha a região</label>
                    <Select options={options} className="mb-6" />
                  </div>
                  <div className="w-1/3">
                    <label className="font-medium">Escolha a versão do modelo</label>
                    <Select options={modelVersion} className="mb-6" />
                  </div>
                </div>
                <label htmlFor="file" className="font-bold">
                  Upload de arquivos
                </label>
                <p>Somente arquivos .jpg e .png. Tamanho máximo de 5 MB.</p>
                <div className="border-dashed flex justify-center items-center border-blue-500 border rounded-lg w-full h-20">
                  <input
                    id="file"
                    name="file"
                    type="file"
                    accept="image/png, image/jpeg"
                    onChange={handleImageChange}
                    className="hidden"
                  />
                  <label htmlFor="file" className="cursor-pointer">
                    Carregue uma imagem
                  </label>
                </div>
              </div>
            </form>

            <div className="w-full h-64 bg-black ml-2 rounded-lg flex justify-center items-center">
              {isLoading ? (
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
              ) : processedImage ? (
                <img
                  src={processedImage}
                  alt="Processed"
                  className="max-w-full max-h-full object-cover w-full h-full rounded-lg"
                />
              ) : (
                <p className="text-white">Pré-visualização da imagem</p>
              )}
            </div>

            <button
              type="button"
              onClick={handleSubmit}
              className="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-4 me-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
            >
              {isLoading ? 'Enviando...' : 'Enviar'}
            </button>
          </div>
        </div>
      </main>
      <section ref={reportSectionRef}>
        {processedComplete && <ReportComponent counted={dataServer.counted} processedImageUrl={dataServer.processed_image_url} colorizeProcessedImageUrl={dataServer.colorize_processed_image_url} modelVersion={dataServer.version} title="Brasil - Sudeste" />}
      </section>
    </div>
  );
}
