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
import { useState, useEffect } from "react";
import Loading from "@/components/loading";
import { Eye, EyeOff } from "lucide-react";

const formSchema = z.object({
  username: z.string().nonempty({ message: "O nome é obrigatório." }).min(3, {
    message: "O nome de usuário deve ter pelo menos 3 caracteres.",
  }),
  password: z.string().nonempty({ message: "A senha é obrigatória." }).min(3, {
    message: "A senha deve ter pelo menos 3 caracteres.",
  }),
});

export default function FormLogin({ onLogin }: any) {
  const navigate = useNavigate();
  const location = useLocation();
  const urlCodigo = new URLSearchParams(location.search);
  const codigo = urlCodigo.get("codigo");
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

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
    setIsLoading(true);

    const data = {
      username: values.username,
      password: values.password,
    };

    AutenticacaoService.login(data)
      .then((response) => {
        if (response.status === 200) {
          localStorage.setItem("access_token", response.data.access_token);
          navigate("/problemas");
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
      })
      .finally(() => setIsLoading(false));
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
                    <Input
                      type="text"
                      {...field}
                      placeholder="Digite seu nome"
                    />
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
                    <div className="relative">
                      <Input
                        type={showPassword ? "text" : "password"}
                        {...field}
                        autoComplete="current-password"
                        placeholder="Digite sua senha"
                      />
                      <button
                        type="button"
                        className="absolute inset-y-0 right-0 p-3 flex items-center text-sm leading-5"
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? (
                          <EyeOff className="h-5 w-5 text-gray-500" />
                        ) : (
                          <Eye className="h-5 w-5 text-gray-500" />
                        )}
                      </button>
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" disabled={isLoading}>
              {isLoading ? <Loading isLoading={isLoading} /> : "Enviar"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}
