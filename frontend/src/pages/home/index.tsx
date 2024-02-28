import { useEffect, useState } from "react";
import problemaService from "../../service/api/problemaService";
import { iDataProblema } from "../../interfaces/iProblema";
import { DataTable } from "../../components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";
import Header from "@/components/header";

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

  const header = [
    { nome: "Problemas", link: "#" },
    { nome: "Turmas", link: "#" },
    { nome: "Torneios", link: "#" },
  ];

  return (
    <>
      <Header options={header} />
      {problemas && problemas.length > 0 ? (
        <div className="mx-[8em]">
          <DataTable columns={problemaColumns} data={problemas} />
        </div>
      ) : (
        <div className="font-bold flex justify-center items-center">
          <p>Não há problemas cadastrados</p>
        </div>
      )}
    </>
  );
}

export default Home;
