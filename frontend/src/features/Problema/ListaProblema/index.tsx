import { useEffect, useState } from "react";
import problemaService from "@/services/models/problemaService";
import { DataTable } from "@/components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Toaster } from "@/components/ui/toaster";
import { useNavigate } from "react-router-dom";
import { iDataProblema } from "@/interfaces/models/iProblema";
import { Separator } from "@/components/ui/separator";
import ImportaProblema from "../Importe/importaProblema";
import Loading from "@/components/loading";
import { toast } from "react-toastify";

function ListaProblema() {
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    handleProblem();
    localStorage.removeItem("aba");
  }, []);

  async function handleProblem() {
    setIsLoading(true);
    await problemaService
      .getProblemas()
      .then((response) => {
        setProblemas(response.data);
      })
      .catch((error) => {
        toast.error(error.response.data.error, {
          autoClose: 5000,
          style: {
            border: "1px solid #e74c3c",
          },
        });
      })
      .finally(() => {
        setIsLoading(false);
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

      {isLoading ? (
        <Loading
          isLoading={isLoading}
          className="text-gray-300 mt-5 w-[3rem] h-[3rem] flex justify-center items-center"
        />
      ) : problemas && problemas.length > 0 ? (
        <div className="mt-4">
          <DataTable
            columns={problemaColumns}
            data={problemas}
            busca
            filtro="nome"
          >
            <Button onClick={cadastraProblema} disabled>
              Cadastrar
            </Button>
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
                <Button onClick={cadastraProblema} disabled>
                  Cadastrar
                </Button>
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
