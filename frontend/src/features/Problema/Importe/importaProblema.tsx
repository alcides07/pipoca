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
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { toast } from "@/components/ui/use-toast";
import problemaService from "@/services/models/problemaService";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const FormSchema = z.object({
  privado: z.boolean().default(false).optional(),
  pacote: z.instanceof(FileList),
});

interface importaProblemaProps {
  handleProblem: () => void;
}

function ImportaProblema({ handleProblem }: importaProblemaProps): JSX.Element {
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
    <AlertDialog open={isOpen} onOpenChange={setIsOpen}>
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
                    <FormLabel>Arquivo</FormLabel>
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

export default ImportaProblema;