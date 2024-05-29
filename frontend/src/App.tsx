import { BrowserRouter } from "react-router-dom";
import Rotas from "./routes";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.min.css";

function App() {
  return (
    <>
      <BrowserRouter>
        <Rotas />
      </BrowserRouter>
      <ToastContainer className="w-[30vw]" position="top-left" draggable />
    </>
  );
}

export default App;
