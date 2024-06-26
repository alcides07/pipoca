import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Checkbox } from "@/components/ui/checkbox";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { toast } from "react-toastify";
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
import linguagensPadrao from "@/utils/linguagem";

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
      message: "O tempo limite deve ter apenas números.",
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
  linguagens: z
    .array(z.string())
    .refine((value: string[]) => value.some((item) => item), {
      message: "Selecione no mínimo uma linguagem.",
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
      tempo_limite: "1000",
      memoria_limite: "256",
    },
    mode: "onChange",
  });

  async function onSubmit(data: ProfileFormValues) {
    await problemaService
      .cadastroProblema(data)
      .then((response) => {
        navigate(`/problema/${response.data.data.id}`);
        toast.success("Problema cadastrado com sucesso!", {
          autoClose: 5000,
          style: {
            border: "1px solid #07bc0c",
          },
        });
      })
      .catch((error) => {
        if (error.response.status === 422) {
          toast.error(
            "O formulário de cadastro foi preenchido incorretamente!",
            {
              autoClose: 5000,
              style: {
                border: "1px solid #e74c3c",
              },
            }
          );
        }
        if (error.response.status === 401) {
          toast.error(error.message, {
            autoClose: 5000,
            style: {
              border: "1px solid #e74c3c",
            },
          });
        }
      });
  }

  return (
    <Card>
      <CardHeader className="">
        <CardTitle className="text-2xl">Cadastro de Problema</CardTitle>
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
                    <FormLabel>Tempo Limite (ms)</FormLabel>
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
                    <FormLabel>Memória Limite (MB)</FormLabel>
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
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="linguagens"
                render={() => (
                  <FormItem>
                    <div className="mb-4">
                      <FormLabel className="text-base">Linguagens</FormLabel>
                      <FormDescription>
                        Selecione as linguagens aceitas na resposta do problema.
                      </FormDescription>
                    </div>
                    {linguagensPadrao.map((linguagem) => (
                      <FormField
                        key={linguagem}
                        control={form.control}
                        name="linguagens"
                        render={({ field }) => {
                          return (
                            <FormItem
                              key={linguagem}
                              className="flex flex-row items-start space-x-3 space-y-0"
                            >
                              <FormControl>
                                <Checkbox
                                  checked={
                                    field.value
                                      ? field.value.includes(linguagem)
                                      : false
                                  }
                                  onCheckedChange={(checked: boolean) => {
                                    return checked
                                      ? field.onChange([
                                          ...(field.value || []),
                                          linguagem,
                                        ])
                                      : field.onChange(
                                          (field.value || []).filter(
                                            (value: string) =>
                                              value !== linguagem
                                          )
                                        );
                                  }}
                                />
                              </FormControl>
                              <FormLabel className="text-sm font-normal">
                                {linguagem}
                              </FormLabel>
                            </FormItem>
                          );
                        }}
                      />
                    ))}

                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="privado"
                render={({ field }) => (
                  <FormItem className="col-span-1">
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
