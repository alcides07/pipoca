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
import AutenticacaoService from "@/services/models/autenticacaoService";
import { toast } from "react-toastify";
import { useState } from "react";
import Loading from "@/components/loading";

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
  onSuccess?: () => void;
}

function FormRegister({ onSuccess }: FormRegisterProps) {
  const [isLoading, setIsLoading] = useState(false);

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
    setIsLoading(true);

    const data = {
      username: values.username,
      email: values.email,
      password: values.password,
      passwordConfirmation: values.passwordConfirmation,
    };

    const Mensagem = ({ email }) => (
      <div>
        Cadastrado realizado com sucesso. Acesse o link de ativação enviado para
        o e-mail <strong>{email}</strong> para ativar sua conta.
      </div>
    );

    AutenticacaoService.register(data)
      .then(() => {
        toast.success(<Mensagem email={values.email} />, {
          progress: undefined,
          autoClose: false,
          style: {
            border: "1px solid #07bc0c",
          },
        });

        if (onSuccess) {
          onSuccess();
        }
      })
      .catch((error) => {
        toast.error(error.response.data.error, {
          autoClose: 5000,
          style: {
            border: "1px solid #e74c3c",
          },
        });
      })
      .finally(() => {
        setIsLoading(false);
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
            <Button type="submit" disabled={isLoading}>
              {isLoading ? <Loading isLoading={isLoading} /> : "Cadastrar"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}

export default FormRegister;
