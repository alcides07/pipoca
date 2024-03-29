import { zodResolver } from "@hookform/resolvers/zod";
import { useFieldArray, useForm } from "react-hook-form";
import { z } from "zod";
import { Link } from "react-router-dom";

import { cn } from "@/lib/utils";
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
import { toast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

const profileFormSchema = z.object({
  privado: z.boolean().default(false).optional(),
  nome: z.string().min(2, {
    message: "O nome de usuário deve ter pelo menos 2 caracteres.",
  }),
  nome_arquivo_entrada: z.string(),
  nome_arquivo_saida: z.string(),
  tempo_limite: z.number().min(250, {
    message: "A entrada deve ser maior ou igual a 250.",
  }),
  memoria_limite: z.number().min(4, {
    message: "A entrada deve ser maior ou igual a 4.",
  }),
});

type ProfileFormValues = z.infer<typeof profileFormSchema>;

// This can come from your database or API.
const defaultValues: Partial<ProfileFormValues> = {
  bio: "I own a computer.",
  urls: [
    { value: "https://shadcn.com" },
    { value: "http://twitter.com/shadcn" },
  ],
};

export default function FormCadastro() {
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues: {
      nome: "",
      privado: true,
      nome_arquivo_entrada: "",
      nome_arquivo_saida: "",
      tempo_limite: 0,
      memoria_limite: 0,
    },
    mode: "onChange",
  });

  const { fields, append } = useFieldArray({
    name: "urls",
    control: form.control,
  });

  function onSubmit(data: ProfileFormValues) {
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="nome"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nome</FormLabel>
              <FormControl>
                <Input placeholder="Informe o nome do problema" {...field} />
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
              {/* <FormDescription>
                  Receive emails about new products, features, and more.
                </FormDescription> */}
              <FormControl>
                {/* <Switch
                  checked={field.value}
                  onCheckedChange={field.onChange}
                  aria-readonly
                /> */}
                <div className="flex items-center space-x-2">
                  <Switch
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                  <Label htmlFor="airplane-mode">Privado</Label>
                </div>
              </FormControl>
            </FormItem>
          )}
        />
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
                <Input placeholder="Informe a memória limite" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Cadastrar</Button>
      </form>
    </Form>
  );
}
