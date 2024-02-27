import { useEffect, useState } from "react";
import problemaService from "../../service/api/problemaService";
import { iDataProblema } from "../../interfaces/iProblema";
import { DataTable } from "../../components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";

function Home() {
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
    <>
      {problemas && problemas.length > 0 ? (
        <div className="w-10/12 ml-12 ">
          <DataTable columns={problemaColumns} data={problemas} />
        </div>
      ) : (
        <div>
          <p>Não há problemas cadastrados</p>
        </div>
      )}
    </>
  );
}

export default Home;
