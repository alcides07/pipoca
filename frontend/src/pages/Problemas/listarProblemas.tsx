import { useEffect, useState } from "react";
import problemaService from "../../service/api/problemaService";
import { iDataProblema } from "../../interfaces/iProblema";
import { DataTable } from "../../components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";

import { Button } from "@/components/ui/button";

import { Card, CardContent } from "@/components/ui/card";
import { Toaster } from "@/components/ui/toaster";
import BotaoImporte from "./components/botaoImporte";
import { useNavigate } from "react-router-dom";

function ListarProblemas() {
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    handleProblem();
  }, []);

  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response.data);
      console.log(response);
    });
  }

  function cadastraProblema(): void {
    navigate("/problemas/cadastro");
  }

  return (
    <div className="px-28">
      <div className="py-4">
        <p className="text-2xl font-bold">Problemas</p>
      </div>
      {problemas && problemas.length > 0 ? (
        <div>
          <DataTable columns={problemaColumns} data={problemas}>
            <Button onClick={cadastraProblema}>Cadastrar</Button>

            <BotaoImporte handleProblem={handleProblem} />
          </DataTable>
        </div>
      ) : (
        <Card className="h-[80vh] flex justify-center items-center">
          <CardContent className="flex flex-col justify-center items-center text-center">
            <div>
              <h1 className="font-bold">Não há problemas cadastrados.</h1>
              <p>Você pode registrar um problema agora!</p>
              <div className="flex flex-col gap-3 m-5">
                <Button onClick={cadastraProblema}>Cadastrar</Button>
                <BotaoImporte handleProblem={handleProblem} />
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      <Toaster />
    </div>
  );
}

export default ListarProblemas;
