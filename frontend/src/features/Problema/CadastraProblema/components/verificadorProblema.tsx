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
import Loading from "@/components/loading";
import type { iProblemaResposta } from "@/interfaces/services/iProblemaResposta";
import ProblemaRespostaService from "@/services/models/problemaRespostaService";
import { DataTable } from "@/components/table";
import { verificadorProblemaColumns } from "@/components/table/columns/verificadorProblemaColumns";

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
  const [rows, setRows] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [verificador, setVerificador] = useState(null);
  const [loadingTesteVerificador, setLoadingTesteVerificador] = useState(true);
  const [testes, setTestes] = useState([]);

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
    consultaVerificador(id);
  }, []);

  async function consultaVerificador(id: number) {
    console.log("Entrei aqui!");
    setLoadingTesteVerificador(true);
    await problemaService.verificadorProblema(id).then((response) => {
      console.log("Verificar", response.data);
      setVerificador(response.data);
      if (response.data && response.data.testes) {
        setTestes(response.data.testes);
      } else {
        setTestes(null);
      }
    });
    setLoadingTesteVerificador(false);
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
            {loadingTesteVerificador ? (
              <Loading
                isLoading={loadingTesteVerificador}
                className="text-gray-300 w-[3rem] h-[3rem] flex justify-center items-center"
              />
            ) : testes != null ? (
              <DataTable
                columns={verificadorProblemaColumns}
                data={testes}
                busca
              >
                <Button variant="outline">Adicionar testes</Button>
                <Button variant="outline">Executar testes</Button>
              </DataTable>
            ) : (
              <div className="flex flex-col justify-center items-center text-center min-h-[50vh]">
                <p>Não há verificador cadastrados.</p>
                <h1 className="font-bold">
                  Por favor, cadastre um verificador e adicione seus testes!
                </h1>
              </div>
            )}
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
