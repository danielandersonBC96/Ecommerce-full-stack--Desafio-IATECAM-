import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/users';

  constructor(private http: HttpClient) { }

  getAuthToken() {
    return sessionStorage.getItem("access_token");
  }

  register(name: string, username: string, password: string): Observable<any> {
    const data = {
      name,
      username,
      password
    };
    return this.http.post(`${this.apiUrl}/createuser`, data);
  }

  login(username: string, password: string): Observable<any> {
    const data = {
      username,
      password
    };

    return this.http.post(`${this.apiUrl}/login`, data, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    });
  }

  logout(): void {
    sessionStorage.removeItem('access_token');
  }

  isAuthenticated(): boolean {
    return !!sessionStorage.getItem('access_token');
  }

  getAccessToken(): string | null {
    return sessionStorage.getItem('access_token');
  }
}
