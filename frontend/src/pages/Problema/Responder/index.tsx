interface ExamplesLayoutProps {
  children?: React.ReactNode;
}

import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import problemaService from "@/service/api/problemaService";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { iDataProblema } from "@/interfaces/iProblema";

function Responder({ children }: ExamplesLayoutProps) {
  const { id } = useParams<{ id: string }>();
  const [problema, setProblema] = useState<iDataProblema>();

  console.log("id", id);

  useEffect(() => {
    getProblem();
  }, []);

  async function getProblem() {
    await problemaService.getProblemaById(id).then((response) => {
      setProblema(response.data);
      console.log(response);
    });
  }

  return (
    <div className="mx-28 my-5 overflow-hidden rounded-[0.5rem] border bg-background shadow-md md:shadow-xl">
      <ResizablePanelGroup direction="vertical" className="min-h-[80vh]">
        <ResizablePanel defaultSize={6}>
          <div className="flex h-full items-center justify-center p-2">
            <span className="font-semibold">Header</span>
          </div>
        </ResizablePanel>
        <ResizableHandle disabled />
        <ResizablePanel defaultSize={94}>
          <ResizablePanelGroup direction="horizontal" className="min-h-[200px]">
            <ResizablePanel defaultSize={60}>
              <div className="flex h-full justify-center px-10">
                {problema && problema.declaracoes[0] && (
                  <div>
                    <h2 className="text-3xl font-bold my-5">
                      {problema.declaracoes[0].titulo}
                    </h2>
                    <p className="pb-5 text-justify">
                      {problema.declaracoes[0].contextualizacao}
                    </p>
                    <div className="pb-5">
                      <span className="text-ms font-bold">Entrada</span>
                      <p>{problema.declaracoes[0].formatacao_entrada}</p>
                    </div>
                    <div className="pb-5">
                      <span className="text-ms font-bold">Saída</span>
                      <p>{problema.declaracoes[0].formatacao_saida}</p>
                    </div>
                  </div>
                )}
              </div>
            </ResizablePanel>
            <ResizableHandle disabled />
            <ResizablePanel defaultSize={40}>
              <div className="flex h-full items-center justify-center p-6">
                <span className="font-semibold">Content</span>
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}

export default Responder;
