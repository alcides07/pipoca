import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Card, CardContent } from "../ui/card";
import { Link, useLocation } from "react-router-dom";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";

interface HeaderProps {
  options: { nome: string; link: string }[];
}

export default function Header({ options }: HeaderProps) {
  const location = useLocation();

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
          <div>
            <Avatar>
              <AvatarImage src="https://github.com/shadcn.png" />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
