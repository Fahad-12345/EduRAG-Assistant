export interface Source {
  file: string;
  page: number;
}

export interface AskResponse {
  answer: string;
  sources: Source[];
}