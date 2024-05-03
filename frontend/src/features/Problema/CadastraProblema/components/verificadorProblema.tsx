import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import problemaService from "@/services/models/problemaService";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/components/ui/use-toast";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import linguagens from "@/utils/linguagem";
import { Toaster } from "@/components/ui/toaster";
import { iDataProblema } from "@/interfaces/models/iProblema";
import Loading from "@/components/loading";
import { iTestesExemplos } from "@/interfaces/models/iTeste";
import type { iProblemaResposta } from "@/interfaces/services/iProblemaResposta";
import ProblemaRespostaService from "@/services/models/problemaRespostaService";
import { DataTable } from "@/components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";

const FormSchema = z.object({
  linguagem: z.string().nonempty("Selecione uma linguagem de programação!"),
  resposta: z
    .string()
    .nonempty("Informe o seu código!")
    .refine(
      (val: string) => val.length >= 10,
      "A resposta deve ter pelo menos 10 caracteres!"
    ),
});

function VerificadorProblema() {
  const { id } = useParams();
  const [problema, setProblema] = useState<iDataProblema>();
  const [rows, setRows] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [testesExemplos, setTestesExemplos] = useState<iTestesExemplos[]>();
  const [loadingProblema, setLoadingProblema] = useState(true);
  const [loadingProblemaExemplos, setLoadingProblemaExemplos] = useState(true);
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      linguagem: "",
      resposta: "",
    },
  });

  async function onSubmit(values: z.infer<typeof FormSchema>) {
    setIsLoading(true);
    const data: iProblemaResposta = {
      resposta: values.resposta,
      linguagem: values.linguagem,
      problema_id: parseInt(id),
    };

    console.log("Resposta", data);

    await ProblemaRespostaService.respondeProblema(data)
      .then(() => {})
      .catch(() => {})
      .finally(() => {
        setIsLoading(false);
      });
  }

  useEffect(() => {
    obtemProblema();
    handleProblem();
  }, []);
  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response.data);
    });
  }

  useEffect(() => {
    if (problema != undefined) obtemTestesExemplos();
  }, [problema]);

  async function obtemProblema() {
    setLoadingProblema(true);

    await problemaService.getProblemaById(id).then((response) => {
      console.log("response.data", response.data);
      setProblema(response.data);
    });
    setLoadingProblema(false);
  }

  async function obtemTestesExemplos() {
    setLoadingProblemaExemplos(true);
    await problemaService.testesExemplosProblema(id).then((response) => {
      console.log("testes:", response.data);
      setTestesExemplos(response.data);
    });
    setLoadingProblemaExemplos(false);
  }

  return (
    <div className="overflow-hidden rounded-[0.5rem] border bg-background shadow-md md:shadow-xl">
      <ResizablePanelGroup direction="horizontal" className="min-h-[300px]">
        <ResizablePanel defaultSize={60}>
          <div className="h-full px-6 py-3">
            <p className="text-3xl font-semibold tracking-tight my-5">
              Testes do Verificador
            </p>
            <Separator className="my-4" />
            <DataTable columns={problemaColumns} data={problemas} busca>
              <Button variant="outline">Adicionar testes</Button>
              <Button variant="outline">Executar testes</Button>
            </DataTable>
          </div>
        </ResizablePanel>
        <ResizableHandle withHandle />
        <ResizablePanel defaultSize={40}>
          <ScrollArea className="h-full w-full px-6">
            <div className="flex h-full justify-center py-6">
              <Button variant="outline" className="w-full" disabled={isLoading}>
                {isLoading ? <Loading isLoading={isLoading} /> : "Importar"}
              </Button>
            </div>
            <Separator />

            <div className="flex h-full justify-center py-6">
              <Form {...form}>
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="w-full space-y-6"
                >
                  <FormField
                    control={form.control}
                    name="linguagem"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Select onValueChange={field.onChange}>
                            <SelectTrigger className="w-full">
                              <SelectValue placeholder="Selecione uma linguagem" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectGroup>
                                {linguagens.map((linguagem: string) => (
                                  <SelectItem key={linguagem} value={linguagem}>
                                    {linguagem}
                                  </SelectItem>
                                ))}
                              </SelectGroup>
                            </SelectContent>
                            <FormMessage />
                          </Select>
                        </FormControl>
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="resposta"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Textarea
                            placeholder="Informe o código do verificador!"
                            className="min-h-[17rem] text-ms"
                            rows={rows}
                            onInput={(e: any) => {
                              setRows(e.target.scrollHeight / 20);
                            }}
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <Button
                    type="submit"
                    className="w-full text-white"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <Loading isLoading={isLoading} />
                    ) : (
                      "Cadastrar"
                    )}
                  </Button>
                </form>
              </Form>
            </div>
          </ScrollArea>
        </ResizablePanel>{" "}
        {/* aqui */}
      </ResizablePanelGroup>
      <Toaster />
    </div>
  );
}

export default VerificadorProblema;
