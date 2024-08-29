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
import { Eye, EyeOff } from "lucide-react";

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
  const [showPassword, setShowPassword] = useState(false);
  const [showPasswordConfirmation, setShowPasswordConfirmation] =
    useState(false);

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

    const Message = ({ email }) => (
      <div>
        Cadastrado realizado com sucesso. Acesse o link de ativação enviado para
        o e-mail <strong>{email}</strong> para ativar sua conta.
      </div>
    );

    AutenticacaoService.register(data)
      .then(() => {
        toast.success(<Message email={values.email} />, {
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
                    <Input
                      autoComplete="off"
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
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>E-mail</FormLabel>
                  <FormControl>
                    <Input
                      type="email"
                      autoComplete="off"
                      {...field}
                      placeholder="Digite seu e-mail"
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
                        autoComplete="off"
                        {...field}
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
            <FormField
              control={form.control}
              name="passwordConfirmation"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirme sua senha</FormLabel>
                  <FormControl>
                    <div className="relative">
                      <Input
                        type={showPasswordConfirmation ? "text" : "password"}
                        autoComplete="off"
                        {...field}
                        placeholder="Confirme sua senha"
                      />
                      <button
                        type="button"
                        className="absolute inset-y-0 right-0 p-3 flex items-center text-sm leading-5"
                        onClick={() =>
                          setShowPasswordConfirmation(!showPasswordConfirmation)
                        }
                      >
                        {showPasswordConfirmation ? (
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
              {isLoading ? <Loading isLoading={isLoading} /> : "Cadastrar"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}

export default FormRegister;
