import { useEffect, useState } from "react";
import problemaService from "../../service/api/problemaService";
import { iDataProblema } from "../../interfaces/iProblema";
import { DataTable } from "../../components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";
import Header from "@/components/header";

function ListarProblema() {
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);

  useEffect(() => {
    handleProblem();
  }, []);

  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response.data);
      console.log(response);
    });
  }

  return (
    <div className="px-28">
      <div className="py-4">
        <p className="text-2xl font-bold">Problemas</p>
      </div>
      {problemas && problemas.length > 0 ? (
        <div>
          <DataTable columns={problemaColumns} data={problemas} />
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
