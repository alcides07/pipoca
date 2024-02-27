import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import problemaService from "../../service/api/problemaService";

function Home() {
  const [problemas, setProblemas] = useState<any[]>([]);

  useEffect(() => {
    handleProblem();
  }, []);

  async function handleProblem() {
    await problemaService.getProblemas().then((response) => {
      setProblemas(response);
      console.log(response);
    });
  }

  return (
    <div>
      <h1 className="text-3xl font-bold underline">Hello world!</h1>
      {problemas.map((problema) => (
        <div key={problema.id}>
          <h2>{problema.nome}</h2>
          <p>{problema.descricao}</p>
        </div>
      ))}
      <Button>Click me</Button>
    </div>
  );
}

export default Home;
