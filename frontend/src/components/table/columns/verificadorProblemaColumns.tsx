import { ColumnDef } from "@tanstack/react-table";
import { Edit2, ClipboardPenLine } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { iTesteVerificador } from "../../../interfaces/models/iTesteVerificador";

export const verificadorProblemaColumns: ColumnDef<iTesteVerificador>[] = [
  {
    accessorKey: "numero",
    header: "Número",
  },
  {
    accessorKey: "entrada",
    header: "Entrada",
  },
  {
    accessorKey: "veredito",
    header: "Status",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const problema = row.original;
      return (
        <div className="px-5 flex flex-row justify-end gap-3">
          <Link to={`/problema/${problema.id}/responde/`}>
            <Button variant="outline" title="Responder">
              <ClipboardPenLine />
            </Button>
          </Link>
          <Link to={`/problema/${problema.id}`}>
            <Button variant="outline" title="Editar">
              <Edit2 />
            </Button>
          </Link>
        </div>
      );
    },
  },
];
