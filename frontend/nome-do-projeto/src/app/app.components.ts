// src/app/app.component.ts

import { Component, OnInit } from '@angular/core';
import { BackendService } from './backend.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  public data: any;

  constructor(private backendService: BackendService) { }

  ngOnInit(): void {
    this.backendService.getData().subscribe(
      (response) => {
        this.data = response;
        console.log('Dados recebidos do backend:', this.data);
      },
      (error) => {
        console.error('Erro ao receber dados do backend:', error);
      }
    );
  }

  public sendDataToBackend(): void {
    const dataToSend = { message: 'Hello from Angular!' };
    this.backendService.sendData(dataToSend).subscribe(
      (response) => {
        console.log('Resposta do backend após enviar dados:', response);
      },
      (error) => {
        console.error('Erro ao enviar dados para o backend:', error);
      }
    );
  }

}
