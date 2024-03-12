import { useEffect, useState } from "react";
import problemaService from "../../service/api/problemaService";
import { iDataProblema } from "../../interfaces/iProblema";
import { DataTable } from "../../components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";

function ListarProblema() {
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);
  const [selectedFile, setSelectedFile] = useState(null);
  useEffect(() => {
    handleProblem();
  }, []);

  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response.data);
      console.log(response);
    });
  }

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    console.log("event", event.target.files[0]);
  };

  return (
    <div className="px-28">
      <div className="py-4">
        <p className="text-2xl font-bold">Problemas</p>
      </div>
      {problemas && problemas.length > 0 ? (
        <div>
          <DataTable
            columns={problemaColumns}
            data={problemas}
            onFileChange={handleFileChange}
          />
        </div>
      ) : (
        <div className="font-bold flex justify-center items-center">
          <p>Não há problemas cadastrados</p>
        </div>
      )}
    </div>
  );
}

export default ListarProblema;
