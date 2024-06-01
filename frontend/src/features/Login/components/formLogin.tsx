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
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

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
      .catch(() => {});
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
