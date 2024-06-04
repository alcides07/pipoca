import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";

import {
  Card,
  CardDescription,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import declaracaoService from "@/services/models/declaracaoService";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { idiomas } from "@/utils/idiomas";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { iDeclaracao } from "@/interfaces/models/iDeclaracao";

const FormSchema = z.object({
  titulo: z.string().nonempty("O título é obrigatório.").max(64, {
    message: "O título da declaração deve ter no máximo 64 caracteres.",
  }),
  idioma: z.string().nonempty("Selecione o idioma!"),
  contextualizacao: z
    .string()
    .nonempty("A contextualização é obrigatória.")
    .max(10240, {
      message: "A contextualização deve ter no máximo 10240 caracteres.",
    }),
  formatacao_entrada: z
    .string()
    .nonempty("A entrada do problema é obrigatória.")
    .max(10240, {
      message: "A entrada do problema deve ter no máximo 10240 caracteres.",
    }),
  formatacao_saida: z
    .string()
    .nonempty("A saída do problema é obrigatória.")
    .max(10240, {
      message: "A saída do problema deve ter no máximo 10240 caracteres.",
    }),
  observacao: z.string().optional(),
  tutorial: z.string().optional(),
  problema_id: z.number(),
});

type ProfileFormValues = z.infer<typeof FormSchema>;

interface FormDeclaracaoProps {
  problemaId: number;
}

function FormDeclaracao({ problemaId }: FormDeclaracaoProps) {
  const [rows, setRows] = useState(1);

  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      titulo: "",
      idioma: "",
      contextualizacao: "",
      formatacao_entrada: "",
      formatacao_saida: "",
      observacao: "",
      tutorial: "",
      problema_id: 0,
    },
    mode: "onChange",
  });

  async function onSubmit(values: ProfileFormValues) {
    const data: iDeclaracao = {
      titulo: values.titulo,
      idioma: values.idioma,
      contextualizacao: values.contextualizacao,
      formatacao_entrada: values.formatacao_entrada,
      formatacao_saida: values.formatacao_saida,
      observacao: values.observacao ?? "",
      tutorial: values.tutorial ?? "",
      problema_id: problemaId ?? null,
    };

    await declaracaoService
      .createDeclaracao(data)
      .then(() => {
        window.scrollTo(0, 0);
        toast({
          title: "Sucesso",
          description: "Declaração cadastrada!",
        });
      })
      .catch(() => {
        toast({
          variant: "destructive",
          title: "Erro.",
          description: "O cadastro de declaração falhou. Tente novamente!",
        });
      });
  }

  return (
    <Card>
      <CardHeader className="">
        <CardTitle>Declaração</CardTitle>
        <CardDescription>
          Para cadastrar as informações do problema, preencha o formulário
          baixo.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Separator className="mb-4" />
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid grid-cols-3 gap-4">
              {" "}
              <FormField
                control={form.control}
                name="titulo"
                render={({ field }) => (
                  <FormItem className="col-span-2">
                    <FormLabel>Título</FormLabel>
                    <FormControl>
                      <Input placeholder="Informe o título" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="idioma"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Idioma</FormLabel>
                    <FormControl>
                      <Select onValueChange={field.onChange}>
                        <SelectTrigger className="w-full">
                          <SelectValue placeholder="Selecione o idioma" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectGroup>
                            {idiomas.map((idioma: string) => (
                              <SelectItem key={idioma} value={idioma}>
                                {idioma}
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
            </div>

            <FormField
              control={form.control}
              name="contextualizacao"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Contextualização</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Informe o contexto do problema"
                      className="min-h-[15rem] text-ms"
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
            <FormField
              control={form.control}
              name="formatacao_entrada"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Entrada</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Informe a entrada do problema"
                      className="min-h-[10rem] text-ms"
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
            <FormField
              control={form.control}
              name="formatacao_saida"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Saída</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Informe a saída do problema"
                      className="min-h-[10rem] text-ms"
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
            <FormField
              control={form.control}
              name="observacao"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Observação</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Informe a observação"
                      className="min-h-[5rem] text-ms"
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
            <FormField
              control={form.control}
              name="tutorial"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Tutorial</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Informe o tutorial do problema"
                      className="min-h-[5rem] text-ms"
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

            <Button className="w-full" type="submit">
              Editar
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
export default FormDeclaracao;
