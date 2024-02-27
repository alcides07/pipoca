import { ColumnDef } from "@tanstack/react-table";
import { iDataProblema } from "../../../interfaces/iProblema";

export const problemaColumns: ColumnDef<iDataProblema>[] = [
  {
    accessorKey: "nome",
    header: "Nome",
  },
  {
    accessorKey: "usuario.username",
    header: "Criador",
  },
  {
    accessorKey: "privado",
    header: "privado",
  },
];
