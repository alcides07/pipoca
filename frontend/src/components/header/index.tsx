import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Card, CardContent } from "../ui/card";

import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";

interface HeaderProps {
  options: { nome: string; link: string }[];
}

export default function Header({ options }: HeaderProps) {
  return (
    <Card className="rounded-none">
      <CardContent className="p-3 flex justify-between">
        <div className="font-bold flex items-center">Juiz Online</div>
        <div>
          <NavigationMenu>
            <NavigationMenuList className="gap-6">
              {options &&
                options.map((option) => (
                  <NavigationMenuItem>
                    <NavigationMenuLink
                      className={navigationMenuTriggerStyle()}
                    >
                      {option.nome}
                    </NavigationMenuLink>
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
  );
}
