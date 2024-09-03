import { ColumnDef } from "@tanstack/react-table";
import { Edit2, FileCode } from "lucide-react";
import { iDataProblema } from "../../../interfaces/models/iProblema";
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
    id: "actions",
    cell: ({ row }) => {
      const problema = row.original;
      return (
        <div className="px-5 flex flex-row justify-end gap-3">
          <Link to={`/problema/${problema.id}/responde/`}>
            <Button variant="outline" title="Responder">
              <FileCode />
            </Button>
          </Link>
          {/* <Link to={`/problema/${problema.id}`}>
            <Button variant="outline" title="Editar" disabled>
              <Edit2 />
            </Button>
          </Link> */}
        </div>
      );
    },
  },
];
