import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import AutenticacaoService from "@/service/api/autenticacaoService";
import { useToast } from "@/components/ui/use-toast";
import { Toaster } from "@/components/ui/toaster";

const formSchema = z.object({
  username: z.string().nonempty({ message: "O nome é obrigatório." }).min(3, {
    message: "O nome de usuário deve ter pelo menos 3 caracteres.",
  }),
  email: z.string().nonempty({ message: "O e-mail é obrigatório." }).email({
    message: "O email deve ser um email válido.",
  }),
  password: z.string().nonempty({ message: "A senha é obrigatória." }).min(3, {
    message: "A senha deve ter pelo menos 3 caracteres.",
  }),

  passwordConfirmation: z
    .string()
    .nonempty({ message: "A confirmação da senha é obrigatória." })
    .min(3, {
      message: "A senha deve ter pelo menos 3 caracteres.",
    }),
});

interface FormRegisterProps {
  onSuccess: () => void;
}

function FormRegister({ onSuccess }: FormRegisterProps) {
  const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      passwordConfirmation: "",
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log("values", values);

    const data = {
      username: values.username,
      email: values.email,
      password: values.password,
      passwordConfirmation: values.passwordConfirmation,
    };
    console.log("data", data);

    AutenticacaoService.register(data)
      .then((response) => {
        console.log("Cadastro", response);
        toast({
          title: "Sucesso.",
          description: "Usuário cadastrado com sucesso!",
          duration: 2000,
        });
        onSuccess();
      })
      .catch((error) => {
        // console.error("Cadastro erro:", error);
        toast({
          variant: "destructive",
          title: "Erro.",
          description: error.response.data.error,
          duration: 2000,
        });
      });
  }
  return (
    <Card>
      <CardHeader>
        <CardTitle>Cadastro</CardTitle>
        <CardDescription>
          Realize cadastro para ter acesso ao sistema Pipoca!
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nome</FormLabel>
                  <FormControl>
                    <Input type="text" placeholder="" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>E-mail</FormLabel>
                  <FormControl>
                    <Input type="email" placeholder="" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Senha</FormLabel>
                  <FormControl>
                    <Input type="password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="passwordConfirmation"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirme sua senha</FormLabel>
                  <FormControl>
                    <Input type="password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit">Cadastrar</Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}

export default FormRegister;
