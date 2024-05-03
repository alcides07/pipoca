import { useEffect, useState } from "react";
import problemaService from "@/services/models/problemaService";
import { DataTable } from "@/components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Toaster } from "@/components/ui/toaster";
import { useNavigate } from "react-router-dom";
import ImportaProblema from "../CadastraProblema/components/importaProblema";
import { iDataProblema } from "@/interfaces/models/iProblema";
import { Separator } from "@/components/ui/separator";

function ListaProblema() {
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    handleProblem();
  }, []);

  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response.data);
    });
  }

  function cadastraProblema(): void {
    navigate("/problema/cadastro");
  }

  return (
    <div>
      <div className="py-4">
        <p className="text-2xl font-bold">Problemas</p>
      </div>
      <Separator />

      {problemas && problemas.length > 0 ? (
        <div className="mt-4">
          <DataTable columns={problemaColumns} data={problemas} busca>
            <Button onClick={cadastraProblema}>Cadastrar</Button>
            <ImportaProblema handleProblem={handleProblem} />
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
                <ImportaProblema handleProblem={handleProblem} />
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      <Toaster />
    </div>
  );
}

export default ListaProblema;
