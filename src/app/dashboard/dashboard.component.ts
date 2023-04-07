import { Component, OnInit} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormControl, FormGroup } from '@angular/forms';
import { Route, Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  fileForm: FormGroup;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fileForm = new FormGroup({
      file: new FormControl('')
    });
  }

  onSubmit() {
    const formData: FormData = new FormData();
    formData.append('file', this.fileForm.get('file').value);

    this.http.post('http://localhost:5000/api/file', formData).subscribe(
      (response) => {
        // Handle successful response
        console.log(response);
      },
      (error) => {
        // Handle error
        console.log(error);
      }
    );
  }
}
