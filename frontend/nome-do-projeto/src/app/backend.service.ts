// src/app/backend.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  private apiUrl = 'http://localhost:8000'; // URL base do seu servidor FastAPI

  constructor(private http: HttpClient) { }

  // Exemplo de método para buscar dados do backend
  public getData(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/data`);
  }

  // Exemplo de método para enviar dados para o backend
  public sendData(data: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/send`, data);
  }
}
