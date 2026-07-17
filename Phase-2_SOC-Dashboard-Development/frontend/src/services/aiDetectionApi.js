import axios from "axios";

const client = axios.create({ baseURL: import.meta.env.VITE_AI_API_BASE_URL || "http://localhost:8002/api", timeout: Number(import.meta.env.VITE_API_TIMEOUT_MS || 10000), headers: { Accept: "application/json" } });
client.interceptors.response.use((response) => response.data, (error) => Promise.reject(new Error(error.response?.data?.error?.message || "AI detection engine is unavailable")));

export const aiDetectionApi = {
  predictions: () => client.get("/ai/predictions", { params: { limit: 20 } }),
  risks: () => client.get("/ai/risk-score", { params: { limit: 20 } }),
  alerts: () => client.get("/ai/alerts", { params: { limit: 20 } }),
};
