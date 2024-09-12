import { Map } from "../../../assets";

export default function HistoryPage() {
  return (
    <div className="p-10">
      <h1 className="mb-8 font-bold text-center text-[#575EA6] text-2xl">Dados relacionados as florestas contabilizadas</h1>

      <div className="relative overflow-x-auto">
        <table className="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3"></th>
              <th scope="col" className="px-6 py-3">
                ID da imagem
              </th>
              <th scope="col" className="px-6 py-3">
                Região
              </th>
              <th scope="col" className="px-6 py-3">
                Data
              </th>
              <th scope="col" className="px-6 py-3">
                Floresta
              </th>
              <th scope="col" className="px-6 py-3">
                Versão do modelo
              </th>
            </tr>
          </thead>
          <tbody>
            {[0, 1, 2, 3].map((item) => (
              <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th
                  scope="row"
                  className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white w-36"
                >
                  <img src={Map} alt="" />
                </th>
                <td className="px-6 py-4">mapa_aurora.png</td>
                <td className="px-6 py-4">Sudeste</td>
                <td className="px-6 py-4">24/08/2024</td>
                <td className="px-6 py-4">Aurora Verde</td>
                <td className="px-6 py-4">v1.0</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
