import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {

  entity = '';
  result:any = null;

  constructor(private http: HttpClient) {}

  analyze() {
    this.http.post('http://localhost:3000/score', {
      entity: this.entity
    }).subscribe(res => {
      this.result = res;
    });
  }
}
