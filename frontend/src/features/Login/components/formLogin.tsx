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
import { useNavigate, useLocation } from "react-router-dom";
import { toast } from "react-toastify";
import { iAtivacao } from "@/interfaces/services/iAutenticacao";
import { useEffect } from "react";

const formSchema = z.object({
  username: z.string().nonempty({ message: "O nome é obrigatório." }).min(3, {
    message: "O nome de usuário deve ter pelo menos 3 caracteres.",
  }),
  password: z.string().nonempty({ message: "A senha é obrigatória." }).min(3, {
    message: "A senha deve ter pelo menos 3 caracteres.",
  }),
});

function FormLogin({ onLogin }: any) {
  const navigate = useNavigate();
  const location = useLocation();
  const urlCodigo = new URLSearchParams(location.search);
  const codigo = urlCodigo.get("codigo");

  useEffect(() => {
    if (codigo) {
      ativacaoConta({ codigo: codigo });
    }
  }, [codigo]);

  function ativacaoConta(data: iAtivacao) {
    AutenticacaoService.ativacao(data)
      .then(() => {
        toast.success("Sua conta foi ativada com sucesso.", {
          autoClose: 5000,
          style: {
            border: "1px solid #07bc0c",
          },
        });
      })
      .catch((error) => {
        toast.error(error.response.data.error, {
          autoClose: 5000,
          style: {
            border: "1px solid #e74c3c",
          },
        });
      });
  }

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    const data = {
      username: values.username,
      password: values.password,
    };

    AutenticacaoService.login(data)
      .then((response) => {
        if (response.status === 200) {
          localStorage.setItem("access_token", response.data.access_token);
          navigate("/dashboard");
          onLogin();
          toast.dismiss();
        }
      })
      .catch((error) => {
        toast.error(error.response.data.error, {
          autoClose: 5000,
          style: {
            border: "1px solid #e74c3c",
          },
        });
      });
  }
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Login</CardTitle>
        <CardDescription>
          Realize login para ter acesso ao sistema Pipoca!
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
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Senha</FormLabel>
                  <FormControl>
                    <Input
                      type="password"
                      {...field}
                      autoComplete="current-password"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit">Entrar</Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}

export default FormLogin;
