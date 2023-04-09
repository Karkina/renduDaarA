import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiCallService } from './api-call-service.service';

@Injectable({
  providedIn: 'root'
})
export class GutenburgAPIService {
  private REST_API_SERVER = 'http://localhost:8000';

  constructor(private httpClient: HttpClient, private apiCall: ApiCallService) { }


  getAll(): any {
    return this.apiCall.getResponseApi(`${this.REST_API_SERVER}/Books/`, null);
  }

  searchOnApi(data: any): any {
    return this.apiCall.getResponseApi(`${this.REST_API_SERVER}/Books/search/${data}`, data);
  }

  getBook(data: any): any {
    return this.apiCall.getResponseApi(`${this.REST_API_SERVER}/Books/text/`, data);
  }

}
