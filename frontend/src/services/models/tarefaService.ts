import axiosInstance from "../axiosInstance";

class TarefaService {
  async tarefa(taskId: string) {
    const response = await axiosInstance.get("/tarefas/", {
      params: {
        uuid: taskId,
      },
    });
    return response.data;
  }
}

export default new TarefaService();
