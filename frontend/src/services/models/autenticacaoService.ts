import axiosInstance from "../axiosInstance";
import {
  iAtivacao,
  iLogin,
  iRegister,
} from "../../interfaces/services/iAutenticacao";

class AutenticacaoService {
  async login(data: iLogin) {
    const response = await axiosInstance.post("/autenticacao/", data, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response;
  }

  async register(data: iRegister) {
    const response = await axiosInstance.post("/usuarios/", data, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    return response;
  }

  async ativacao(data: iAtivacao) {
    const response = await axiosInstance.post("/autenticacao/ativacao/", data);
    return response;
  }
}

export default new AutenticacaoService();
