import {Component, OnInit, Output} from '@angular/core';
import {EnvironmentsApi} from '../../api/api/EnvironmentsApi';
import generate_name from './random_name';
import {Environment} from "../../api/model/Environment";
import {MatSnackBar} from "@angular/material";
import {FormControl, Validators} from "@angular/forms";

@Component({
  selector: 'app-environments-list',
  templateUrl: './environmentslist.component.html',
  styleUrls: ['./environmentslist.component.css'],
  providers: [EnvironmentsApi]
})
export class EnvironmentsListComponent implements OnInit {
  public environments: Environment[] = [];

  public nameValidators: FormControl[] = [];

  @Output()
  public errorMessage?: string = null;

  constructor(private api: EnvironmentsApi, private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.updateDisplay();
  }

  public addEnvironment(): void {
    this.api.createEnvironment({name: generate_name()}).subscribe(
      x => this.updateDisplay(),
      this.onError
    );
  }

  public removeEnvironment(idx: number): void {
    const id = this.environments[idx].id;
    this.api.deleteEnvironment(id).subscribe(x => this.updateDisplay(), this.onError);
  }

  public updateEnvironment(idx: number): void {
    const id = this.environments[idx].id;
    const name = this.environments[idx].name;
    this.api.updateEnvironment(id, {name: name}).subscribe(x => this.updateDisplay(), this.onError);
  }

  private updateDisplay(): void {
    this.environments = [];

    this.api.getEnvironments().subscribe(
      d => {
        this.environments = d;
        this.nameValidators = [];
        for (let i = 0; i < this.environments.length; ++i) {
          this.nameValidators[i] = new FormControl('', [
            Validators.required,
            Validators.pattern(/^[^/]+$/)
          ]);
        }
      },
      this.onError
    );
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
    this.snackBar.open(this.errorMessage, 'OK');
  }
}
