import Select from "react-select";
import { useState } from "react";
import ReportComponent from "../../../components/Report";

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
  const [processedComplete, setProcessedComplete] = useState<boolean>(false);


  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files === null ){
      return;
    }

    const file = e.target.files[0];

    if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
      setSelectedImage(file);
    } else {
      alert('Please select a valid image file (PNG or JPEG)');
    }
  };

  const handleSubmit = async () => {
    setProcessedComplete(true);
    if (!selectedImage) {
      alert('Please select an image first.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await fetch('http://0.0.0.0:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        alert('Ok');
        setProcessedComplete(true);
        setProcessedImage(data.processedImageUrl);
      } else {
        alert('Failed to upload image.');
      }
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div>
      <main className="flex flex-col my-14 px-14 py-8 gap-y-10 items-center">
        <div className="w-1/2">
          <h1 className="font-bold text-[#575EA6]">Teste de modelo</h1>
          <p>
            O ESG é uma das tendências mais relevantes de mercado dos últimos
            tempos. Convidamos você a fazer parte do nosso universo de
            abundância.
          </p>
        </div>
        <div className="flex flex-col w-1/2">
          <div className="flex flex-col gap-y-10">
            <form >
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
                <label htmlFor="file-upload" className="font-bold">
                  Upload files
                </label>
                <p>
                  Somente arquivos .jpg e .png. Tamanho máximo de arquivo de 5 MB.
                </p>
                <div className="border-dashed flex justify-center items-center border-blue-500 border rounded-lg w-full h-20">
                  <input
                    id="file-upload"
                    type="file"
                    accept="image/png, image/jpeg"
                    onChange={handleImageChange}
                    className="hidden"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    Carregue uma imagem
                  </label>
                </div>
              </div>
            </form>
            <div className="w-full h-64 bg-black ml-2 rounded-lg flex justify-center items-center">
              {processedImage ? (
                <img
                  src={processedImage}
                  alt="Processed"
                  className="max-w-full max-h-full object-contain rounded-lg"
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
            Enviar
          </button>
          </div>

        </div>
      </main>
      <section>
          {processedComplete && <ReportComponent value={90} title="io" />}
        </section>
    </div>
  );
}
