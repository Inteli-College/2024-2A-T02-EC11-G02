import Select from "react-select";

const options = [
  { value: "brasil-sudeste", label: "Brasil - Sudeste" },
  { value: "brasil-sul", label: "Brasil - Sul" },
  { value: "brasil-nordeste", label: "Brasil - Nordeste" },
  { value: "brasil-norte", label: "Brasil - Norte" },
  { value: "brasil-centro-oeste", label: "Brasil - Centro-Oeste" },
];

export default function UploadPage() {
  return (
    <div>
      <div className="flex my-14 justify-evenly px-14 py-8">
        <div className="w-1/3">
          <h1 className="font-bold text-[#575EA6]">Teste de modelo</h1>
          <p>
            O ESG é uma das tendências mais relevantes de mercado dos últimos
            tempos. Convidamos você a fazer parte do nosso universo de
            abundância.
          </p>
        </div>
        <div className="flex flex-col w-1/2 ">
          <div className="flex">
            <div>
              <label className="font-bold">Escolha a região</label>
              <Select options={options} className="mb-6" />
              <label htmlFor="" className="font-bold">
                Upload files
              </label>
              <p>
                Somente arquivos .jpg e .png. Tamanho máximo de arquivo de 5 MB.
              </p>
              <div className="border-dashed flex justify-center items-center border-blue-500 border rounded-lg w-full h-20">
                Carregue uma imagem
              </div>
              {/* <input type="file" /> */}
            </div>
            <div className="w-full h-64 bg-black ml-2 rounded-lg"></div>
          </div>
          <button type="button" className=" w-28 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Enviar</button>
        </div>
      </div>
    </div>
  );
}
