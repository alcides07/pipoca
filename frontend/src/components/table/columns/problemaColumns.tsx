import { ColumnDef } from "@tanstack/react-table";
import { iDataProblema } from "../../../interfaces/iProblema";
import { ArrowUpDown, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";

export const problemaColumns: ColumnDef<iDataProblema>[] = [
  {
    accessorKey: "nome",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Nome
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
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
