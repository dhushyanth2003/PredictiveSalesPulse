import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormControl, FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';


interface signupresponse {
  status: {
    statusCode: number
  }
}

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit{
  signup:FormGroup|any;
  constructor(private http: HttpClient, private router: Router) {}
  
  
  
  ngOnInit(): void{
    this.signup=new FormGroup({
      'username':new FormControl(),
      'password':new FormControl(),
      'email':new FormControl()
    })
  }

  signupdata(signup:FormGroup){ 
    console.log(this.signup.value);
    this.http.post<signupresponse>('http://localhost:5000/api/register-user', this.signup.value).subscribe((response: any) => {
      if(response.status && response.status.statusCode == 200){
       
        this.router.navigate(['/']);
        alert("Signup Successfully completed");
      }
      else{
        alert("User doesn't exist");
      }
    });
  }

  

  }  