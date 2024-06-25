import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent {
  name: string = '';
  username: string = '';
  password: string = '';

  constructor(
    private authService: AuthService,
    private router: Router,
    private messageService: MessageService
  ) { }

  signup(signupForm: NgForm) {
    if (signupForm.valid) {
      this.authService.register(this.name, this.username, this.password).subscribe({
        next: (response) => {
          console.log("User registration successful", response);
          this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Account created successfully' });
          this.router.navigate(["/login"]);
        },
        error: (error) => {
          console.log("Error during registration", error);
          this.messageService.add({ severity: 'error', summary: 'Error', detail: 'Registration failed' });
        }
      });
    }
  }
}
