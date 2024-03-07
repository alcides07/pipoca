import axiosInstance from "../axiosInstance";
import { iLogin, iRegister } from "../../interfaces/iAutenticacao";

class AutenticacaoService {
  async login(data: iLogin) {
    const response = await axiosInstance.post("/auth", data);
    return response;
  }

  async register(data: iRegister) {
    const response = await axiosInstance.post("/users", data);
    return response;
  }
}

export default new AutenticacaoService();
