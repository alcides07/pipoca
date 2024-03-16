import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Card, CardContent } from "../ui/card";
import { Link, useLocation } from "react-router-dom";
import { LogOut } from "lucide-react";
import { Popcorn } from "lucide-react";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { useNavigate } from "react-router-dom";

interface HeaderProps {
  options: { nome: string; link: string }[];
}

export default function Header({ options }: HeaderProps): JSX.Element {
  const location = useLocation();
  const navigate = useNavigate();

  function handleLogout(): void {
    localStorage.removeItem("access_token");
    navigate("/");
  }

  return (
    <div>
      <Card className="rounded-none px-28">
        <CardContent className="px-0 py-3 flex justify-between">
          <div className="font-bold flex items-center ">Juiz Online</div>
          <div>
            <NavigationMenu>
              <NavigationMenuList className="gap-6">
                {options &&
                  options.map((option) => (
                    <NavigationMenuItem key={option.nome}>
                      <Link
                        to={option.link}
                        className={`
                          ${navigationMenuTriggerStyle()}
                          ${
                            location.pathname === option.link ||
                            (option.link === "/" && location.pathname === "/")
                              ? "selected"
                              : ""
                          }
                        `}
                      >
                        {option.nome}
                      </Link>
                    </NavigationMenuItem>
                  ))}
              </NavigationMenuList>
            </NavigationMenu>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Avatar>
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>CN</AvatarFallback>
              </Avatar>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-25">
              <DropdownMenuItem>
                <LogOut className="mr-2 h-4 w-4" />
                <button onClick={handleLogout}>Sair</button>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </CardContent>
      </Card>
    </div>
  );
}
