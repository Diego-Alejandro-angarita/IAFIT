import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Seedbed } from '../models/seedbed.model';

@Injectable({
  providedIn: 'root'
})
export class SeedbedsService {
  private apiUrl = 'http://127.0.0.1:8001/api/seedbeds/';

  constructor(private http: HttpClient) {}

  getSeedbeds(faculty: string = '', search: string = ''): Observable<Seedbed[]> {
    const params: string[] = [];

    if (faculty) params.push(`faculty=${encodeURIComponent(faculty)}`);
    if (search) params.push(`search=${encodeURIComponent(search)}`);

    let url = this.apiUrl;
    if (params.length) {
      url += '?' + params.join('&');
    }

    return this.http.get<Seedbed[]>(url);
  }

  getSeedbed(id: number): Observable<Seedbed> {
    return this.http.get<Seedbed>(`${this.apiUrl}${id}/`);
  }
}