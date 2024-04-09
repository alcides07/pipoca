import { ColumnDef } from "@tanstack/react-table";
import { Edit2, ClipboardPenLine } from "lucide-react";
import { iDataProblema } from "../../../interfaces/models/iProblema";
import { ArrowUpDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

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
  {
    id: "actions",
    cell: ({ row }) => {
      const problema = row.original;
      return (
        <div className="w-5 flex flex-row gap-3">
          <Link to={`/problema/${problema.id}/responde/`}>
            <Button variant="outline" title="Responder">
              <ClipboardPenLine />
            </Button>
          </Link>
          <Link to={`/editar/${problema.id}`}>
            <Button variant="outline" title="Editar">
              <Edit2 />
            </Button>
          </Link>
        </div>
      );
    },
  },
];
