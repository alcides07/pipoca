import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import problemaService from "@/services/models/problemaService";
import { useState, useEffect } from "react";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormLabel,
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
import { DataTable } from "@/components/table";
import { verificadorProblemaColumns } from "@/components/table/columns/verificadorProblemaColumns";
import type { iVerificadorService } from "@/interfaces/services/iVerificador";
import { Input } from "@/components/ui/input";
import verificadorService from "@/services/models/verificadorService";
import { toast } from "react-toastify";
import type {
  iTesteVerificador,
  iVerificador,
} from "@/interfaces/models/iVerificador";
import ImportaVerificador from "../../Importe/importaVerificador";

const FormSchema = z.object({
  nome: z
    .string()
    .min(3, {
      message: "O nome do verificador deve ter pelo menos 3 caracteres.",
    })
    .max(64, {
      message: "O nome do verificador deve ter no máximo 64 caracteres.",
    }),
  linguagem: z.string().nonempty("Selecione uma linguagem de programação!"),
  corpo: z
    .string()
    .nonempty("Informe o seu código!")
    .min(10, {
      message: "O código do verificador deve ter pelo menos 10 caracteres.",
    })
    .max(250000, {
      message: "O código do verificador deve ter no máximo 250000 caracteres.",
    }),
});

interface EditaVerificadorProps {
  problemaId: number;
}

function EditaVerificador({ problemaId }: EditaVerificadorProps) {
  const [rows, setRows] = useState<number>(1);
  const [idVerificador, setIdVerificador] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [verificador, setVerificador] = useState<iVerificador>();
  const [loadingTesteVerificador, setLoadingTesteVerificador] =
    useState<boolean>(true);
  const [testes, setTestes] = useState<iTesteVerificador[]>([]);

  useEffect(() => {
    if (problemaId) {
      consultaVerificador(problemaId);
    }
  }, []);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {},
    mode: "onChange",
  });

  async function consultaVerificador(id: number) {
    await problemaService.verificadorProblema(id).then((response) => {
      setIdVerificador(response.data.id);
      if (response.data != undefined) {
        form.reset({
          nome: response.data.nome,
          linguagem: response.data.linguagem,
          corpo: response.data.corpo,
        });
      }

      setVerificador(response.data);

      if (response.data && response.data.testes) {
        setTestes(response.data.testes);
      } else {
        setTestes([]);
      }
    });
    setLoadingTesteVerificador(false);
  }

  async function onSubmit(values: z.infer<typeof FormSchema>) {
    setIsLoading(true);

    const data: iVerificadorService = {
      nome: values.nome,
      corpo: values.corpo,
      linguagem: values.linguagem,
      problema_id: problemaId,
    };

    await verificadorService
      .atualizaVerificador(idVerificador, data)
      .then(() => {
        window.scrollTo(0, 0);
        toast.success("Verificador atualizado com sucesso!", {
          autoClose: 5000,
          style: {
            border: "1px solid #07bc0c",
          },
        });
        consultaVerificador(problemaId);
      })
      .catch(() => {
        window.scrollTo(0, 0);
        toast.error("A Atualização do verificador falhou. Tente novamente!", {
          autoClose: 5000,
          style: {
            border: "1px solid #e74c3c",
          },
        });
      });

    setIsLoading(false);
  }

  return (
    <div className="overflow-hidden rounded-[0.5rem] border bg-background shadow-md md:shadow-xl">
      <ResizablePanelGroup direction="horizontal" className="min-h-[300px]">
        <ResizablePanel defaultSize={60}>
          <div className="h-full px-6 py-3">
            <p className="text-2xl font-semibold tracking-tight my-5">
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
                filtro="entrada"
                mensagem="Não há testes cadastrados!"
              >
                <Button variant="outline">Adicionar testes</Button>
                <Button variant="outline">Executar testes</Button>
              </DataTable>
            ) : verificador != null ? (
              <DataTable
                columns={verificadorProblemaColumns}
                data={testes}
                busca
                filtro="entrada"
                mensagem="Não há testes cadastrados!"
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
            <div className="flex h-full justify-center py-6 px-1">
              {isLoading ? (
                <Loading isLoading={isLoading} />
              ) : (
                <ImportaVerificador
                  problemaId={problemaId}
                  verificador={verificador}
                />
              )}
            </div>
            <Separator />

            <div className="flex h-full justify-center py-6">
              <Form {...form}>
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="w-full space-y-6 px-1"
                >
                  <FormField
                    control={form.control}
                    name="nome"
                    render={({ field }) => (
                      <FormItem>
                        {/* <FormLabel>Nome</FormLabel> */}
                        <FormControl>
                          <Input placeholder="Nome do verificador" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="linguagem"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Idioma</FormLabel>
                        <FormControl>
                          <Select
                            value={field.value}
                            onValueChange={field.onChange}
                          >
                            <SelectTrigger className="w-full">
                              <SelectValue placeholder="Selecione uma linguagem" />
                            </SelectTrigger>
                            <SelectContent className="h-56">
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
                    name="corpo"
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
                    onClick={() => {
                      form.handleSubmit(onSubmit)();
                    }}
                  >
                    {isLoading ? (
                      <Loading isLoading={isLoading} />
                    ) : (
                      "Editar Verificador"
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

export default EditaVerificador;
