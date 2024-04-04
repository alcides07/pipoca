import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { useState, useEffect } from "react";

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import problemaService from "@/service/api/problemaService";
import { Separator } from "@/components/ui/separator";
import { useParams } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";
import { Progress } from "@/components/ui/progress";

const profileFormSchema = z.object({
  privado: z.boolean().default(false).optional(),
  nome: z
    .string()
    .min(3, {
      message: "O nome do problema deve ter pelo menos 3 caracteres.",
    })
    .max(64, {
      message: "O nome do problema deve ter no máximo 64 caracteres.",
    }),
  nome_arquivo_entrada: z
    .string()
    .nonempty("O nome do arquivo de entrada é obrigatório.")
    .max(64, {
      message: "O nome do arquivo de entrada deve ter no máximo 64 caracteres.",
    }),
  nome_arquivo_saida: z
    .string()
    .nonempty("O nome do arquivo de saida é obrigatório.")
    .max(64, {
      message: "O nome do arquivo de saída deve ter no máximo 64 caracteres.",
    }),
  tempo_limite: z
    .string()
    .refine((val: string): boolean => /^[0-9]+$/.test(val), {
      message: "O tempo limite deve ser apenas números.",
    })
    .transform((val: string): number => Number(val))
    .refine((value: number): boolean => value >= 250, {
      message: "O tempo limite deve ser maior ou igual a 250.",
    })
    .refine((value: number): boolean => value <= 150000, {
      message: "O tempo limite deve ser menor ou igual a 150000.",
    }),

  memoria_limite: z
    .string()
    .refine((val: string): boolean => /^[0-9]+$/.test(val), {
      message: "O tempo limite deve ser apenas números.",
    })
    .transform((val: string): number => Number(val))
    .refine((value: number): boolean => value >= 4, {
      message: "A memória limite deve ser maior ou igual a 4.",
    })
    .refine((value: number): boolean => value <= 1024, {
      message: "A memória limite deve ser menor ou igual a 1024.",
    }),
});

type ProfileFormValues = z.infer<typeof profileFormSchema>;

function FormCadastroTabs() {
  const { id } = useParams<{ id: string }>();
  const [problema, setProblema] = useState<any>();
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    window.scrollTo(0, 0);
    getProblema();
  }, []);

  async function getProblema() {
    await problemaService.getProblemaById(id).then((response) => {
      setProblema(response.data);
      setLoading(false);
      form.reset({
        nome: response.data.nome,
        privado: response.data.privado,
        nome_arquivo_entrada: response.data.nome_arquivo_entrada,
        nome_arquivo_saida: response.data.nome_arquivo_saida,
        tempo_limite: response.data.tempo_limite,
        memoria_limite: response.data.memoria_limite,
      });
    });
  }

  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    mode: "onChange",
  });

  async function onSubmit(data: ProfileFormValues) {
    const p: ProfileFormValues = {
      nome: data.nome,
      privado: data.privado,
      nome_arquivo_entrada: data.nome_arquivo_entrada,
      nome_arquivo_saida: data.nome_arquivo_saida,
      tempo_limite: data.tempo_limite,
      memoria_limite: data.memoria_limite,
    };

    await problemaService.updateProblema(id, p).then((response: any) => {
      console.log("data na atualização", response.data);
      toast({
        title: "Sucesso.",
        description: "Problema atualizado!",
        duration: 3000,
      });
    });
  }

  return loading ? (
    <Progress data-state="loading" className="w-full" />
  ) : (
    <Card>
      <CardHeader>
        <CardTitle>Cadastro de Problema</CardTitle>
        <CardDescription>
          Preencha o formulário para cadastrar um problema.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Separator className="my-4" />
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-12">
            <FormField
              control={form.control}
              name="nome"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nome</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Informe o nome do problema"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="privado"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <div className="flex items-center space-x-2">
                      <Switch
                        // checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                      <Label htmlFor="airplane-mode">Privado</Label>
                    </div>
                  </FormControl>
                </FormItem>
              )}
            />
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="nome_arquivo_entrada"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nome do Arquivo de Entrada</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Informe o nome do arquivo de entrada"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="nome_arquivo_saida"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nome do Arquivo de Saída</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Informe o nome do arquivo de saída"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="tempo_limite"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Tempo Limite</FormLabel>
                    <FormControl>
                      <Input placeholder="Informe o tempo limite" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="memoria_limite"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Memória Limite</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="Informe a memória limite"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <Button className="w-full" type="submit">
              Cadastrar
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
export default FormCadastroTabs;
