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
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import problemaService from "@/services/models/problemaService";
import { Separator } from "@/components/ui/separator";
import { useNavigate } from "react-router-dom";

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

function FormCadastro() {
  const navigate = useNavigate();

  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: {
      nome: "",
      privado: false,
      nome_arquivo_entrada: "",
      nome_arquivo_saida: "",
      tempo_limite: 0,
      memoria_limite: 0,
    },
    mode: "onChange",
  });

  async function onSubmit(data: ProfileFormValues) {
    await problemaService
      .createProblema(data)
      .then((response) => {
        navigate(`/problema/${response.data.data.id}`);
        toast({
          title: "Sucesso",
          description: "Problema criado!",
        });
      })
      .catch(() => {
        toast({
          variant: "destructive",
          title: "Erro.",
          description: "O cadastro de problema falhou. Tente novamente!.",
        });
      });
  }

  return (
    <Card>
      <CardHeader className="">
        <CardTitle className="text-3xl">Cadastro de Problema</CardTitle>
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
export default FormCadastro;