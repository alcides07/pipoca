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
import { iDataProblema } from "@/interfaces/iProblema";

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
import linguagens from "../../../utils/linguagem";

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

interface RespondeProblemaProps {
  children?: React.ReactNode;
}

function RespondeProblema({ children }: RespondeProblemaProps) {
  const { id } = useParams<{ id: string }>();
  const [problema, setProblema] = useState<iDataProblema>();
  const [rows, setRows] = useState(1);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      linguagem: "",
      resposta: "",
    },
  });

  function onSubmit(data: z.infer<typeof FormSchema>) {
    console.log("data", data);
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }

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
    <div className="overflow-hidden rounded-[0.5rem] border bg-background shadow-md md:shadow-xl">
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
              <ScrollArea className="h-full w-full">
                <div className="flex h-full justify-center overflow-y-auto px-10">
                  {problema && problema.declaracoes[0] && (
                    <div>
                      <h2 className="text-3xl font-bold my-5">
                        {problema.declaracoes[0].titulo}
                      </h2>
                      <Separator className="my-4" />

                      <p className="pb-5 text-justify">
                        {problema.declaracoes[0].contextualizacao}
                      </p>
                      <div className="pb-5">
                        <span className="text-ms font-bold">Entrada</span>
                        <p>{problema.declaracoes[0].formatacao_entrada}</p>
                      </div>
                      <div>
                        <span className="text-ms font-bold">Saída</span>
                        <p>{problema.declaracoes[0].formatacao_saida}</p>
                      </div>
                      <Separator className="my-4" />
                    </div>
                  )}
                </div>
              </ScrollArea>
            </ResizablePanel>
            <ResizableHandle withHandle />
            <ResizablePanel defaultSize={40}>
              <ScrollArea className="h-full w-full">
                <div className="flex h-full justify-center p-6">
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
                                    {linguagens.map((linguagem: any) => (
                                      <SelectItem
                                        key={linguagem}
                                        value={linguagem}
                                      >
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
                                placeholder="Tell us a little bit about yourself"
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
                      <Button type="submit" className="w-full">
                        Enviar
                      </Button>
                    </form>
                  </Form>
                </div>
              </ScrollArea>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}

export default RespondeProblema;
