import { Checkbox } from "@/components/ui/checkbox";
import {
  Form,
  FormControl,
  FormDescription,
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
import problemaService from "@/services/models/problemaService";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "react-toastify";
import linguagensPadrao from "@/utils/linguagem";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

const FormSchema = z.object({
  privado: z.boolean().default(false).optional(),
  pacote: z.instanceof(FileList),
  linguagens: z
    .array(z.string())
    .refine((value: string[]) => value.some((item) => item), {
      message: "Selecione no mínimo uma linguagem.",
    }),
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
    console.log("values 1", values);

    const formData = new FormData();
    formData.append("pacote", values.pacote[0]);
    formData.append("privado", String(values.privado));
    values.linguagens.forEach((linguagem: string, index: number) => {
      formData.append(`linguagens[${index}]`, linguagem);
    });

    for (var pair of formData.entries()) {
      console.log(pair[0] + ", " + pair[1]);
    }

    problemaService
      .uploadFile(formData)
      .then(() => {
        handleProblem();
        toast.success("Problema Importado!", {
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
            <div className="grid grid-cols-2 gap-4 pt-5">
              <FormField
                control={form.control}
                name="linguagens"
                render={() => (
                  <FormItem>
                    <div className="mb-4">
                      <FormLabel className="text-base">Linguagens</FormLabel>
                      <FormDescription>
                        Selecione as linguagens aceitas na resposta do problema.
                      </FormDescription>
                    </div>
                    {linguagensPadrao.map((linguagem) => (
                      <FormField
                        key={linguagem}
                        control={form.control}
                        name="linguagens"
                        render={({ field }) => {
                          return (
                            <FormItem
                              key={linguagem}
                              className="flex flex-row items-start space-x-3 space-y-0"
                            >
                              <FormControl>
                                <Checkbox
                                  checked={
                                    field.value
                                      ? field.value.includes(linguagem)
                                      : false
                                  }
                                  onCheckedChange={(checked) => {
                                    return checked
                                      ? field.onChange([
                                          ...(field.value || []),
                                          linguagem,
                                        ])
                                      : field.onChange(
                                          (field.value || []).filter(
                                            (value) => value !== linguagem
                                          )
                                        );
                                  }}
                                />
                              </FormControl>
                              <FormLabel className="text-sm font-normal">
                                {linguagem}
                              </FormLabel>
                            </FormItem>
                          );
                        }}
                      />
                    ))}

                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="privado"
                render={({ field }) => (
                  <FormItem className="col-span-1">
                    <FormControl>
                      <div className="flex items-center space-x-2">
                        <Switch
                          // checked={field.value}
                          onCheckedChange={field.onChange}
                        />
                        <Label htmlFor="airplane-mode">Privado</Label>
                      </div>
                    </FormControl>
                  </FormItem>
                )}
              />
            </div>
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
