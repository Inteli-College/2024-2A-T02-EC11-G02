import { Link } from "react-router-dom";
import { Abundance, Ares } from "../../assets";
import { Outlet } from "react-router-dom";

const NavbarComponent = () => {
  return (
    <div className="h-screen">
      <nav className="bg-[#2C2F53] border-gray-200 dark:bg-gray-900 h-20">
        <div className=" flex flex-wrap items-center justify-between mx-auto p-4">
          <div className="flex">
            <div
              className="flex items-center space-x-3 rtl:space-x-reverse"
            >
              <img src={Abundance} className="h-8" alt="Abundance logo" />
            </div>
            <div
              className="hidden w-full md:block md:w-auto"
              id="navbar-default"
            >
              <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg  md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 ">
                <li>
                  <Link
                    className="block py-2 px-3 text-white bg-transparent"
                    aria-current="page"
                    to="/app/reports"
                  >
                    Relatórios
                  </Link>
                </li>
                <li>
                  <Link
                    to="/app/upload"
                    className="block py-2 px-3 text-white bg-transparent"
                    aria-current="page"
                  >
                    Upload
                  </Link>
                </li>

                <li>
                  <Link
                    aria-current="page"
                    to="/app/history"
                    className="block py-2 px-3 text-white bg-transparent"
                  >
                    Histórico
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <img src={Ares} className="h-8" alt="Abundance logo" />
        </div>
      </nav>
      <div className="h-full">
        <Outlet />
      </div>
    </div>
  );
};

export default NavbarComponent;
