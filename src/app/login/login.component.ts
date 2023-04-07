import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

interface LoginResponse {
  status: {
    statusCode: number
  }
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  login: FormGroup | any;
  
  constructor(private http: HttpClient, private router: Router) {}
  
  ngOnInit(): void {
    this.login = new FormGroup({
      'email': new FormControl(),
      'password': new FormControl()
    });
  }
  
  logindata(login: FormGroup) { 
    console.log(this.login.value);
    this.http.post<LoginResponse>('http://localhost:5000/api/login', this.login.value).subscribe((response) => {
      
      if(response.status && response.status.statusCode == 200){
          this.router.navigate(['/dash'])
      }
      else{
        alert("User doesn't exist")
      }
    });

  }
}
