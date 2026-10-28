const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export interface PredictionResponse {
  input: string;
  prediction: unknown;
}

export interface AnalyzeResponse {
  input_text: string;
  prediction: unknown;
  document_id: string | number;
}

export type ResearchResponse = AnalyzeResponse;

export interface APIError {
  detail?: string;
  message?: string;
}

class ApiService {
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData: APIError = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.message || 'API request failed');
    }
    return response.json();
  }

  async predict(text: string, language: string = "en"): Promise<PredictionResponse> {
    const response = await fetch(`${API_BASE_URL}/api/predict/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text, language }),
    });
    
    return this.handleResponse<PredictionResponse>(response);
  }

  async analyze(data: { text?: string; file?: File; voice?: File; language?: string }): Promise<AnalyzeResponse> {
    const response = await fetch(`${API_BASE_URL}/api/analyze/`, {
      method: "POST",
      body: this.buildMultipartPayload(data),
    });

    return this.handleResponse<AnalyzeResponse>(response);
  }

  async research(data: { text?: string; file?: File; voice?: File; language?: string }): Promise<ResearchResponse> {
    const response = await fetch(`${API_BASE_URL}/api/research/`, {
      method: "POST",
      body: this.buildMultipartPayload(data),
    });

    return this.handleResponse<ResearchResponse>(response);
  }

  // Health check endpoint
  async healthCheck(): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/`);
    return this.handleResponse<{ message: string }>(response);
  }

  // Legal Entity Intelligence endpoints
  async analyzeEntitiesText(text: string, language: string = "en"): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/entities/analyze-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, language }),
    });
    return this.handleResponse<any>(response);
  }

  async analyzeEntitiesFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${API_BASE_URL}/api/entities/analyze-file`, {
      method: "POST",
      body: formData,
    });
    return this.handleResponse<any>(response);
  }

  async redactEntities(text: string, labels?: string[]): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/entities/redact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, labels }),
    });
    return this.handleResponse<any>(response);
  }

  getEntitiesExportCsvUrl(text: string): string {
    return `${API_BASE_URL}/api/entities/export/csv?text=${encodeURIComponent(text)}`;
  }


  private buildMultipartPayload(data: { text?: string; file?: File; voice?: File; language?: string }): FormData {
    const formData = new FormData();

    if (data.text) {
      formData.append("text", data.text);
    }

    if (data.file) {
      formData.append("file", data.file);
    }

    if (data.voice) {
      formData.append("voice", data.voice);
    }

    if (data.language) {
      formData.append("language", data.language);
    }

    return formData;
  }
}

export const apiService = new ApiService();