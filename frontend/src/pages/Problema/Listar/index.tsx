import { useEffect, useState } from "react";
import problemaService from "../../../service/api/problemaService";
import { iDataProblema } from "../../interfaces/iProblema";
import { DataTable } from "../../../components/table";
import { problemaColumns } from "@/components/table/columns/problemaColumns";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
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
import { Card, CardContent } from "@/components/ui/card";
import { Toaster } from "@/components/ui/toaster";
import { toast } from "@/components/ui/use-toast";

const FormSchema = z.object({
  privado: z.boolean().default(false).optional(),
  pacote: z.instanceof(FileList),
});

function TableButton({ handleProblem }: () => void): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      privado: false,
    },
  });

  const fileRef = form.register("pacote");

  function onSubmit(values: z.infer<typeof FormSchema>) {
    const formData = new FormData();
    formData.append("pacote", values.pacote[0]);
    formData.append("privado", String(values.privado));

    problemaService
      .uploadFile(formData)
      .then(() => {
        handleProblem();
        toast({
          title: "Sucesso.",
          description: "Problema Importado!",
          duration: 3000,
        });
      })
      .catch((error) => {
        toast({
          variant: "destructive",
          title: "Erro.",
          description: error.response.data.error,
          duration: 3000,
        });
      });
  }

  return (
    <AlertDialog isOpen={isOpen} onDismiss={() => setIsOpen(false)}>
      <AlertDialogTrigger asChild>
        <Button variant="outline">Importar</Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogTitle>Importe um problema</AlertDialogTitle>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-1">
            <FormField
              control={form.control}
              name="pacote"
              render={() => {
                return (
                  <FormItem>
                    <FormLabel>File</FormLabel>
                    <FormControl>
                      <Input type="file" placeholder="shadcn" {...fileRef} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                );
              }}
            />
            <FormField
              control={form.control}
              name="privado"
              render={({ field }) => (
                <FormItem className="flex flex-row items-start space-x-3 space-y-0 rounded-md p-3 m-0">
                  <FormControl>
                    <Checkbox
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                  <div className="leading-none">
                    <FormLabel>Privado?</FormLabel>
                  </div>
                </FormItem>
              )}
            />
          </form>
        </Form>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={() => setIsOpen(false)}>
            Cancel
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

import { useNavigate } from "react-router-dom";

function Listar() {
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    handleProblem();
  }, []);

  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response.data);
      console.log(response);
    });
  }

  function responde(): void {
    localStorage.removeItem("access_token");
    navigate("/");
  }

  return (
    <div className="px-28">
      <div className="py-4">
        <p className="text-2xl font-bold">Problemas</p>
      </div>
      {problemas && problemas.length > 0 ? (
        <div>
          <DataTable columns={problemaColumns} data={problemas}>
            <TableButton handleProblem={handleProblem} />
          </DataTable>
        </div>
      ) : (
        <Card className="h-[80vh] flex justify-center items-center">
          <CardContent className="flex flex-col justify-center items-center text-center">
            <div>
              <h1 className="font-bold">Não há problemas cadastrados.</h1>
              <p>Você pode registrar um problema agora!</p>
              <div className="flex flex-col gap-3 m-5">
                <Button onClick={responde}>Cadastrar</Button>
                <TableButton handleProblem={handleProblem} />
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      <Toaster />
    </div>
  );
}

export default Listar;
