import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import TarefaService from "@/services/models/tarefaService";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

import { Toaster } from "@/components/ui/toaster";
import { Badge } from "@/components/ui/badge";
import Loading from "@/components/loading";
import Latex from "react-latex";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { iDataProblema } from "@/interfaces/models/iProblema";
import problemaService from "@/services/models/problemaService";
import { useParams } from "react-router-dom";

function ResultadoProblema() {
  const location = useLocation();
  const { taskId } = location.state || {};
  console.log("taskId:", taskId);

  const [resultadoResposta, setResultadoResposta] = useState<any>();
  const [loadingResultado, setLoadingResultado] = useState(true);
  const [problema, setProblema] = useState<iDataProblema>();
  const { id: idParam } = useParams();
  const id = Number(idParam);

  useEffect(() => {
    tarefa(taskId);
    obtemProblema();
  }, []);

  useEffect(() => {
    console.log("resultadoResposta", resultadoResposta);
  }, [resultadoResposta]);

  async function tarefa(taskId: string) {
    setLoadingResultado(true);

    await TarefaService.tarefa(taskId).then((response) => {
      console.log("testes:", response.data);
      setResultadoResposta(response.data);
    });
    setLoadingResultado(false);
  }

  async function obtemProblema() {
    setLoadingResultado(true);

    await problemaService.getProblemaById(id).then((response) => {
      console.log("response.data", response.data);
      setProblema(response.data);
    });
    setLoadingResultado(false);
  }

  return (
    <div className="overflow-hidden rounded-[0.5rem] border bg-background shadow-md md:shadow-xl">
      <ResizablePanelGroup direction="vertical" className="min-h-[80vh]">
        <ResizablePanel defaultSize={8}>
          <ResizablePanelGroup direction="horizontal">
            <ResizablePanel
              defaultSize={30}
              className="m-1 flex justify-center items-center"
            >
              <span className="text-xs font-bold flex justify-center">
                Memória Limite
              </span>
              <span className="p-3">|</span>
              <Badge className="py-0" variant="secondary">
                {problema?.memoria_limite} MB
              </Badge>
            </ResizablePanel>
            <ResizableHandle disabled className="bg-white" />
            <ResizablePanel
              defaultSize={30}
              className="m-1 flex justify-center items-center"
            >
              <span className="text-xs font-bold flex justify-center">
                Tempo Limite
              </span>
              <span className="p-3">|</span>
              <Badge className=" py-0" variant="secondary">
                {problema?.tempo_limite} ms
              </Badge>
            </ResizablePanel>
            <ResizableHandle disabled className="bg-white" />
            <ResizablePanel
              defaultSize={40}
              className="m-1 px-0 h-full flex justify-center items-center"
            >
              <span className="text-xs font-bold flex justify-center">
                Tags
              </span>
              <span className="p-3">|</span>
              <span className="">
                {problema?.tags?.map((tag) => (
                  <Badge variant="secondary" key={tag.id} className="py-0 m-1">
                    {tag?.nome}{" "}
                  </Badge>
                ))}
              </span>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={92}>
          <ResizablePanelGroup direction="horizontal" className="min-h-[200px]">
            <ResizablePanel defaultSize={100}>
              {problema != undefined && problema != null ? (
                <ScrollArea className="h-full w-full">
                  <div className="flex h-full w-full px-10">
                    {problema && problema.declaracoes[0] && (
                      <div className="w-full">
                        <h2 className="text-2xl font-bold my-5">
                          {problema.declaracoes[0].titulo}
                        </h2>
                        <Separator className="my-4" />
                        {/* {testesExemplos != undefined ? (
                          <Table className="border rounded mb-8">
                            <TableHeader className="bg-slate-100">
                              <TableRow className="divide-y divide-slate-200">
                                <TableHead className="text-center">
                                  Exemplos de Entrada
                                </TableHead>
                                <TableHead className="text-center">
                                  Exemplos de Saída
                                </TableHead>
                              </TableRow>
                            </TableHeader>
                            <TableBody>
                              {testesExemplos.map((teste, index) => (
                                <TableRow key={index}>
                                  <TableCell className="border rounded">
                                    {teste.entrada}
                                  </TableCell>
                                  <TableCell className="">
                                    {teste.saida}
                                  </TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        ) : (
                          <Loading
                            isLoading={loadingResultado}
                            className="text-gray-300 w-[3rem] h-[3rem] flex justify-center items-center"
                          />
                        )} */}
                      </div>
                    )}
                  </div>
                </ScrollArea>
              ) : (
                <Loading
                  className="text-gray-300 w-[3rem] h-[3rem] flex justify-center items-center"
                  isLoading={loadingResultado}
                  divHeight="h-full"
                />
              )}
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup>
      <Toaster />
    </div>
  );
}

export default ResultadoProblema;
