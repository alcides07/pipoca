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
import { Card, CardContent } from "@/components/ui/card";

function ResultadoProblema() {
  const location = useLocation();
  const { taskId } = location.state || {};

  const [resultadoResposta, setResultadoResposta] = useState<any>();
  const [loadingResultado, setLoadingResultado] = useState(true);
  const [problema, setProblema] = useState<iDataProblema>();
  const { id: idParam } = useParams();
  const id = Number(idParam);

  useEffect(() => {
    if (taskId) {
      tarefa(taskId);
    }
    obtemProblema();
  }, []);

  useEffect(() => {}, [resultadoResposta]);

  async function tarefa(taskId: string) {
    setLoadingResultado(true);

    await TarefaService.tarefa(taskId).then((response) => {
      const { saida_usuario, saida_esperada, veredito } = response.resultado;
      setResultadoResposta({ saida_usuario, saida_esperada, veredito });
    });
    setLoadingResultado(false);
  }

  async function obtemProblema() {
    setLoadingResultado(true);

    await problemaService.getProblemaById(id).then((response) => {
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
          {problema != undefined && problema != null ? (
            <ScrollArea className="h-full w-full">
              <div className="flex h-full w-full px-10">
                {problema && problema.declaracoes[0] && (
                  <div className="w-full">
                    <h2 className="text-2xl font-bold my-5">
                      {`${problema.declaracoes[0].titulo} - RESULTADOS`}
                    </h2>
                    <Separator className="my-4" />
                    {resultadoResposta ? (
                      resultadoResposta.saida_usuario.length > 0 &&
                      resultadoResposta.saida_esperada.length > 0 &&
                      resultadoResposta.veredito.length > 0 ? (
                        <Table className="border rounded mb-8">
                          <TableHeader className="bg-slate-100">
                            <TableRow className="divide-y divide-slate-200">
                              <TableHead className="text-center">
                                Saída do Usuário
                              </TableHead>
                              <TableHead className="text-center">
                                Saída Esperada
                              </TableHead>
                              <TableHead className="text-center">
                                Veredito
                              </TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {resultadoResposta.saida_usuario.map(
                              (saida, index) => (
                                <TableRow key={index}>
                                  <TableCell className="border rounded">
                                    {saida}
                                  </TableCell>
                                  <TableCell className="border rounded">
                                    {resultadoResposta.saida_esperada[index]}
                                  </TableCell>
                                  <TableCell className="border rounded">
                                    {resultadoResposta.veredito[index]}
                                  </TableCell>
                                </TableRow>
                              )
                            )}
                          </TableBody>
                        </Table>
                      ) : (
                        <Card className="h-[50vh] flex justify-center items-center">
                          <CardContent className="flex flex-col justify-center items-center text-center">
                            <div>
                              <p className="font-bold">
                                Seu código não passou nos testes do problema!
                              </p>
                            </div>
                          </CardContent>
                        </Card>
                      )
                    ) : (
                      <Loading
                        isLoading={loadingResultado}
                        className="text-gray-300 w-[3rem] h-[3rem] flex justify-center items-center"
                      />
                    )}
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
      <Toaster />
    </div>
  );
}

export default ResultadoProblema;
