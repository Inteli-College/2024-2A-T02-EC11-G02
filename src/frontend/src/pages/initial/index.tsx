

export default function InitialPage() {
  return (
    <div
      className={`text-white bg-gradient-background h-screen w-full flex flex-col items-center justify-center`}
    >
      <div className="w-[600px]">
        <span className="uppercase">Ecossistema Syntropy</span>
        <h1 className="mt-5 font-bold text-6xl">
          Quantas árvores estamos plantando?{" "}
        </h1>
        <p className="mt-5">
          O ESG é uma das tendências mais relevantes de mercado dos últimos
          tempos. Veja abaixo nosso crescimento do universo de abundância.
        </p>
        <button
          type="button"
          onClick={() => {
            window.location.href = "/app";
          }}
          className="text-white mt-5 hover:text-black hover:bg-white border border-whit focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 "
        >
          Acessar relatórios
        </button>
      </div>
    </div>
  );
}
