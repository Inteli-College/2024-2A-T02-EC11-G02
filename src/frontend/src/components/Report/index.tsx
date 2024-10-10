import { useState } from "react";

interface ReportComponentProps {
  title: string;
  modelVersion: string;
  counted: number;
  processedImageUrl: string;
  colorizeProcessedImageUrl: string;
}

const ReportComponent: React.FC<ReportComponentProps> = ({
  title,
  modelVersion,
  counted,
  processedImageUrl,
  colorizeProcessedImageUrl,
}) => {
  // Array de URLs das imagens
  const images = [processedImageUrl, colorizeProcessedImageUrl];

  // Estado para armazenar o índice atual do carrossel
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  // Função para alternar para a próxima imagem
  const nextImage = () => {
    setCurrentImageIndex((prevIndex) => 
      prevIndex === images.length - 1 ? 0 : prevIndex + 1
    );
  };

  return (
    <div className="bg-neutral-200 w-full h-full min-h-96">
      <div className="py-24 flex flex-col gap-12">
        <div className="flex justify-between items-center mx-24 px-5">
          <div>
            <h1 className="text-[#575EA6] font-bold text-3xl">{title}</h1>
            <p className="max-w-screen-md mt-2">
              O ESG é uma das tendências mais relevantes de mercado dos últimos
              tempos. Convidamos você a fazer parte do nosso universo de
              abundância.
            </p>
          </div>
          <h1 className="text-[#575EA6] font-bold text-3xl">
            Versão do modelo {modelVersion.toUpperCase()}
          </h1>
        </div>

        <div className="flex justify-between mx-24 px-5">
          {/* Carrossel */}
          <div>
            <div id="carroseul" className="relative w-full max-w-lg mx-auto">
              {/* Imagem atual */}
              <img
                src={images[currentImageIndex]}
                alt="Imagem do modelo"
                className="w-auto max-w-xs rounded-lg"
              />

              {/* Botão próximo */}
              <button
                onClick={nextImage}
                className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-blue-500 text-white px-2 py-1 m-4 rounded-full"
              >
                &#8594;
              </button>
            </div>
          </div>
          <div >
            <h1>Dados da Análise</h1>
            <ul className="p-5 rounded-sm bg-slate-50 w-[600px]">
              <li>Árvores contadas: {counted}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportComponent;
