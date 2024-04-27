import axiosInstance from "../axiosInstance";
import type { iProblemaResposta } from "@/interfaces/services/iProblemaResposta";

class ProblemaRespostaService {
  async respondeProblema(data: iProblemaResposta) {
    const response = await axiosInstance.post(`/problemasRespostas/`, data);
    return response;
  }
}

export default new ProblemaRespostaService();
