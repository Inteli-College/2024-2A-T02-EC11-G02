import { Graph, Map } from "../../../assets";

export default function ReportsPage() {
  return (
    <div className="text-white flex h-full justify-around bg-[#2C2F53] p-5">
      <div className="flex gap-28 justify-between mx-24 my-14">
        <div className="w-full">
          <h1 className="font-bold text-2xl text-[#C2C7F5]">Mapa árvores x hectares</h1>
          
          <p className="mb-8">
            Os aspectos ambientais consideram o desempenho de uma empresa como
            zeladora da natureza. Os critérios ambientais consideram o desempenho
            de uma empresa como zeladora da natureza dos acionistas. O mapa abaixo
            se refere a Floresta Aurora Verde.{" "}
          </p>
          <img src={Map} alt="Mapa" className="max-w-lg" />
        </div>
        <div className="w-full">
          <h1 className="font-bold text-2xl text-[#C2C7F5]">Quantidade de captura de carbono</h1>
          <p className="mb-8">Captura de carbono mensurado da Floresta Aurora Verde. </p>
          <img src={Graph} alt="graph" className="mb-8"/>
          <h1 className="font-bold text-2xl text-[#C2C7F5]">Quantidade de carbono</h1>
          <p>
            O ESG é uma das tendências mais relevantes de mercado dos últimos
            tempos. Convidamos você a fazer parte do nosso universo de abundância.
          </p>
        </div>
      </div>
    </div>
  );
}
