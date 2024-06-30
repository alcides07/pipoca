import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { toast } from "react-toastify";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { iVerificadorService } from "@/interfaces/services/iVerificador";
import verificadorService from "@/services/models/verificadorService";

const FormSchema = z.object({
  verificador: z.instanceof(FileList),
});

interface ImportaVerificadorProps {
  problemaId: number;
  verificador: any;
}

function ImportaVerificador({
  problemaId,
  verificador,
}: ImportaVerificadorProps): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);
  console.log("Verificador do importe:", verificador);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {},
  });

  const fileRef = form.register("verificador");

  async function onSubmit(values: z.infer<typeof FormSchema>) {
    const formData = new FormData();
    formData.append("verificador", values.verificador[0]);

    // Acessando o arquivo
    const arquivo: any = formData.get("verificador");

    // Criando um novo FileReader
    const leitor = new FileReader();

    // Lendo o arquivo como texto
    leitor.readAsText(arquivo);

    leitor.onload = async function (event) {
      // Verificando se event.target.result não é null
      if (event.target && event.target.result) {
        let conteudo = event.target.result as string;

        // Obtendo a extensão do arquivo
        const extensao = arquivo.name
          .split(".")
          .pop() as keyof typeof mapaExtensaoLinguagem;

        // Mapeando a extensão para a linguagem
        const mapaExtensaoLinguagem = {
          cpp: "cpp.g++17",
          java: "java11",
          py: "python.3",
          rb: "ruby.3",
        };

        const linguagem = mapaExtensaoLinguagem[extensao];

        const data: iVerificadorService = {
          nome: arquivo.name,
          corpo: conteudo,
          linguagem: linguagem,
          problema_id: problemaId,
        };

        if (verificador) {
          await verificadorService
            .atualizaVerificador(verificador.id, data)
            .then(() => {
              window.scrollTo(0, 0);
              localStorage.setItem("V", JSON.stringify(true));
              window.location.reload();
            })
            .catch(() => {
              window.scrollTo(0, 0);
              toast.error(
                "O cadastro do verificador falhou. Tente novamente!",
                {
                  autoClose: 5000,
                  style: {
                    border: "1px solid #e74c3c",
                  },
                }
              );
            });
        } else {
          await verificadorService
            .criaVerificador(data)
            .then(() => {
              window.scrollTo(0, 0);
              localStorage.setItem("V", JSON.stringify(true));
              window.location.reload();
            })
            .catch(() => {
              window.scrollTo(0, 0);
              toast.error(
                "O cadastro do verificador falhou. Tente novamente!",
                {
                  autoClose: 5000,
                  style: {
                    border: "1px solid #e74c3c",
                  },
                }
              );
            });
        }
      }
    };
  }

  return (
    <AlertDialog open={isOpen} onOpenChange={setIsOpen}>
      <AlertDialogTrigger asChild className="w-full">
        <Button variant="outline">Importar Verificador</Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogTitle>Importe um verificador</AlertDialogTitle>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-1">
            <FormField
              control={form.control}
              name="verificador"
              render={() => {
                return (
                  <FormItem>
                    <FormLabel>Arquivo</FormLabel>
                    <FormControl>
                      <Input type="file" placeholder="shadcn" {...fileRef} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                );
              }}
            />
          </form>
        </Form>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={() => setIsOpen(false)}>
            Cancelar
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={() => {
              setIsOpen(false);
              form.handleSubmit(onSubmit)();
            }}
          >
            Importar
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

export default ImportaVerificador;
