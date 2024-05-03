import axiosInstance from "../axiosInstance";

class VerificadorService {
  async consultaTesteVerificador(id: number) {
    const response = await axiosInstance.get(`/verificadores/${id}/testes`);
    return response.data;
  }
}

export default new VerificadorService();
