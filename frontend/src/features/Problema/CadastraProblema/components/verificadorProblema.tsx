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
import type { iProblemaResposta } from "@/interfaces/services/iProblemaResposta";
import ProblemaRespostaService from "@/services/models/problemaRespostaService";
import verificadorService from "@/services/models/verificadorService";
import { DataTable } from "@/components/table";
import { verificadorProblemaColumns } from "@/components/table/columns/verificadorProblemaColumns";
import { iTesteVerificador } from "@/interfaces/models/iTesteVerificador";

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
  const [verificador, setVerificador] = useState(null);
  const [loadingProblema, setLoadingProblema] = useState(true);
  const [loadingProblemaExemplos, setLoadingProblemaExemplos] = useState(true);
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);
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
    obtemProblema();
  }, []);

  useEffect(() => {
    if (problema) {
      async function fetchVerificador() {
        await consultaVerificador(problema.id);
      }
      fetchVerificador();
    }
  }, [problema]);

  // if (problema) {
  //   useEffect(() => {
  //     consultaVerificador(problema.id);
  //   }, [problema.id]);
  // }

  async function consultaVerificador(id: number) {
    setIsLoading(true);
    await problemaService.verificadorProblema(id).then((response) => {
      console.log("Verificar", response.data);
      setVerificador(response.data);
      if (response.data && response.data.testes) {
        setTestes(response.data.testes);
      } else {
        setTestes(null);
      }
    });
    setIsLoading(false);
  }

  async function obtemProblema() {
    setLoadingProblema(true);

    await problemaService.getProblemaById(id).then((response) => {
      console.log("response.data", response.data);
      setProblema(response.data);
    });
    setLoadingProblema(false);
  }

  useEffect(() => {
    console.log("verificador 2", verificador);
  }, [verificador]);

  return (
    <div className="overflow-hidden rounded-[0.5rem] border bg-background shadow-md md:shadow-xl">
      <ResizablePanelGroup direction="horizontal" className="min-h-[300px]">
        <ResizablePanel defaultSize={60}>
          <div className="h-full px-6 py-3">
            <p className="text-3xl font-semibold tracking-tight my-5">
              Testes do Verificador
            </p>
            <Separator className="my-4" />
            {isLoading ? (
              <Loading isLoading={isLoading} />
            ) : verificador ? (
              <DataTable
                columns={verificadorProblemaColumns}
                data={problema}
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
