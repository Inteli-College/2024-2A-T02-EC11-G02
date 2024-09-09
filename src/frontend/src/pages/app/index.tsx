import NavbarComponent from "../../components/Navbar";
import NavbarRoutes from "./navbatRoutes";

export default function AppPage() {
  return (
    <div className="flex flex-col h-screen">
      <NavbarComponent />
      <div className="flex-grow">
        <NavbarRoutes />
      </div>
    </div>
  );
}
