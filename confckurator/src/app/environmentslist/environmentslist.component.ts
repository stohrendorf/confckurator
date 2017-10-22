import {Component, OnInit, Output} from '@angular/core';
import {FormArray, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {EnvironmentsApi} from '../../api/api/EnvironmentsApi';
import generate_name from './random_name';

@Component({
  selector: 'app-environments-list',
  templateUrl: './environmentslist.component.html',
  styleUrls: ['./environmentslist.component.css'],
  providers: [FormBuilder, EnvironmentsApi]
})
export class EnvironmentsListComponent implements OnInit {
  public environmentsForm: FormGroup;
  public environmentsList: FormArray;

  @Output()
  public errorMessage?: string = null;

  constructor(private api: EnvironmentsApi, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
    this.environmentsList = this.formBuilder.array([]);
    this.environmentsForm = this.formBuilder.group({
      environments: this.environmentsList
    });

    this.updateDisplay();
  }

  public addEnvironment(): void {
    this.api.createEnvironment({name: generate_name()}).subscribe(
      x => this.updateDisplay(),
      this.onError
    );
  }

  public removeEnvironment(idx: number): void {
    const id = this.environmentsList.controls[idx].get('id').value;
    this.api.deleteEnvironment(id).subscribe(x => this.updateDisplay(), this.onError);
  }

  private updateDisplay(): void {
    while (this.environmentsList.length > 0) {
      this.environmentsList.removeAt(0);
    }

    this.api.getEnvironments().subscribe(
      d => d.forEach(e => this.environmentsList.push(this.formBuilder.group({
        name: [
          {value: e.name, disabled: e.in_use}, Validators.pattern(/[^/]+$/)
        ],
        id: [e.id]
      }))),
      this.onError
    );
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
  }
}
