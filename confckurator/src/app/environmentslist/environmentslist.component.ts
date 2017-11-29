import {Component, OnInit, Output} from '@angular/core';
import {EnvironmentsApi} from '../../api/api/EnvironmentsApi';
import generate_name from './random_name';
import {Environment} from "../../api/model/Environment";

@Component({
  selector: 'app-environments-list',
  templateUrl: './environmentslist.component.html',
  styleUrls: ['./environmentslist.component.css'],
  providers: [EnvironmentsApi]
})
export class EnvironmentsListComponent implements OnInit {
  public environments: Environment[] = [];

  @Output()
  public errorMessage?: string = null;

  constructor(private api: EnvironmentsApi) {
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
      d => this.environments = d,
      this.onError
    );
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
  }
}
