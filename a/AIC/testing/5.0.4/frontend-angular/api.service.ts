import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ApiService {

  constructor(private http: HttpClient) {}

  getScore(entity: string) {
    return this.http.post('http://localhost:3000/score', { entity });
  }

  getHistory(entity: string) {
    return this.http.get(`http://localhost:3000/history/${entity}`);
  }
}
