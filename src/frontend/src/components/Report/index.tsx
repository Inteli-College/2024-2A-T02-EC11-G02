import { Link } from "react-router-dom";
import { Abundance, Ares } from "../../assets";
import { Outlet } from "react-router-dom";

interface ReportComponentProps {
  title: string;
  value: number;
}


const ReportComponent: React.FC<ReportComponentProps> = ({ title, value }) =>  {

  
  return (
    <div className="bg-neutral-600 w-full h-full">
      <div className="flex justify-between items-center p-4">
        <h1 className="text-white text-lg">{title}</h1>
        <h1 className="text-white text-lg">{value}</h1>
      </div>
    </div>
  );
};

export default ReportComponent;
