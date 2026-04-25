import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent {

  entity = '';
  scoreData: any;
  historyData: any;

  constructor(private api: ApiService) {}

  search() {

    this.api.getScore(this.entity).subscribe(res => {
      this.scoreData = res;
    });

    this.api.getHistory(this.entity).subscribe(res => {
      this.historyData = res;
    });
  }
}
