import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  plotUrl!: string;
  inputNumber!: number;
  selectedSeason!: string;
  constructor(private http: HttpClient) {}

  onSubmit(event: Event) {
    event.preventDefault();
    console.log(this.inputNumber);
    console.log(this.selectedSeason);

    // Create a FormData object to send file
    const formData: FormData = new FormData();
    formData.append('file', (event.target as HTMLFormElement)['file'].files[0]);
    formData.append('number', this.inputNumber.toString());
    formData.append('season', this.selectedSeason);

    // Send POST request to Flask API to generate plot
    this.http.post<any>('http://localhost:5000/api/file', formData, { responseType: 'json' }).subscribe(result => {
      // Set the plotUrl variable with the base64-encoded image
      this.plotUrl = `data:image/png;base64, ${result.plot}`;
    });
  }
}
