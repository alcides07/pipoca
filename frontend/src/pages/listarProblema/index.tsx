import { useEffect, useState } from "react";
import problemaService from "../../service/api/problemaService";
import { iDataProblema } from "../../interfaces/iProblema";
import { DataTable } from "../../components/table";
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
// import { toast } from "@/components/ui/use-toast";

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
import { toast } from "@/components/ui/use-toast";

const FormSchema = z.object({
  privado: z.boolean().default(false).optional(),
  pacote: z
    .string()
    .refine((value: any) => value !== "", "O campo file é obrigatório"),
});

function TableButton(): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      privado: false,
      pacote: "",
    },
  });

  function onSubmit(values: z.infer<typeof FormSchema>) {
    console.log("values", values);
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
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <div className="grid w-full items-start gap-1.5">
                      <Input id="picture" type="file" {...field} />
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
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
            {/* <Button type="submit" style={{ display: "none" }}>
              Entrar
            </Button> */}
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

function ListarProblema() {
  const [problemas, setProblemas] = useState<iDataProblema[]>([]);
  useEffect(() => {
    handleProblem();
  }, []);

  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response.data);
      console.log(response);
    });
  }

  return (
    <div className="px-28">
      <div className="py-4">
        <p className="text-2xl font-bold">Problemas</p>
      </div>
      {problemas && problemas.length > 0 ? (
        <div>
          <DataTable columns={problemaColumns} data={problemas}>
            <TableButton />
          </DataTable>
        </div>
      ) : (
        <div className="font-bold flex justify-center items-center">
          <p>Não há problemas cadastrados</p>
        </div>
      )}
    </div>
  );
}

export default ListarProblema;
