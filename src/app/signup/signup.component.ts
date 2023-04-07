import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { NgIfContext } from '@angular/common';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit{
  signup:FormGroup|any;
  constructor(private http: HttpClient){}
  
  
  ngOnInit(): void{
    this.signup=new FormGroup({
      'fname':new FormControl(),
      'lname':new FormControl(),
      'password':new FormControl(),
      'email':new FormControl()
    })
  }

  signupdata(signup:FormGroup){ 
    console.log(this.signup.value);
    this.http.post('http://localhost:5000/api/register-user', this.signup.value).subscribe((response: any) => {
      console.log(response);
      
    });
  }
}
