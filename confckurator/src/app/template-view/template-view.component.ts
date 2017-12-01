import {Component, Input, OnInit, Output} from '@angular/core';
import {AbstractControl, FormArray, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {TemplatesApi} from '../../api';
import {Template} from '../../api';
import {Variable} from '../../api';
import {Observable} from 'rxjs/Observable';
import {IdResponse} from '../../api';
import {List} from 'linqts';
import {MatSnackBar} from "@angular/material";

@Component({
  selector: 'app-template-view',
  templateUrl: './template-view.component.html',
  styleUrls: ['./template-view.component.css'],
  providers: [FormBuilder, TemplatesApi]
})
export class TemplateViewComponent implements OnInit {
  public variablesForm: FormGroup;
  public variablesList: FormArray;
  public code = '';

  @Output()
  public errorMessage?: string = null;

  private variablesToDelete: number[] = [];

  private activeTemplate: Template;

  constructor(private api: TemplatesApi, private formBuilder: FormBuilder, private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.variablesList = this.formBuilder.array([]);
    this.variablesForm = this.formBuilder.group({
      variables: this.variablesList
    });
  }

  @Input()
  public set template(tpl: Template) {
    this.activeTemplate = tpl;
    this.load();
  }

  public get template(): Template {
    return this.activeTemplate;
  }

  private load(): void {
    if (this.activeTemplate == null || this.activeTemplate.id == null) {
      return;
    }

    this.api.getTemplate(this.activeTemplate.id, true).subscribe(t => {
      this.activeTemplate.name = t.name;
      this.activeTemplate.variables = t.variables;
      this.activeTemplate.text = t.text;
      this.updateDisplay();
    }, this.onError);
  }

  public createVariable(variable: Variable = null): FormGroup {
    return this.formBuilder.group({
      name: [
        {value: variable == null ? '' : variable.name, disabled: variable != null && variable.in_use},
        Validators.pattern(/^[a-zA-Z_][a-zA-Z0-9_]*$/)
      ],
      description: [!variable ? '' : variable.description],
      id: [!variable ? null : variable.id]
    });
  }

  private updateDisplay(): void {
    while (this.variablesList.length > 0) {
      this.variablesList.removeAt(0);
    }

    this.activeTemplate.variables.forEach(v => {
      this.variablesList.push(this.createVariable(v));
    });

    this.code = this.activeTemplate.text;
  }

  public save(): void {
    if (this.activeTemplate.id == null) {
      this.api.createTemplate({name: this.activeTemplate.name, text: ''}).subscribe(tpl => {
        this.activeTemplate.id = tpl.id;
        this.sendSaveRequest();
      }, this.onError);
    } else {
      this.sendSaveRequest();
    }
  }

  private sendSaveRequest(): Observable<IdResponse> {
    const request = this.api
      .updateTemplate(this.activeTemplate.id, {
        name: this.activeTemplate.name,
        text: this.code,
        variables: {
          create: new List<AbstractControl>(this.variablesList.controls)
            .Where(c => c.get('id').value == null)
            .Select(c => {
              return {
                name: c.get('name').value,
                description: c.get('description').value
              };
            })
            .ToArray(),
          delete: this.variablesToDelete,
          update: new List<AbstractControl>(this.variablesList.controls)
            .Where(c => c.get('id').value != null)
            .Select(c => {
              return {
                id: c.get('id').value,
                description: c.get('description').value,
                name: c.get('name').value
              };
            })
            .ToArray()
        }
      });
    this.variablesToDelete = [];

    request.subscribe(x => this.load(), this.onError);

    return request;
  }

  public addVariable(): void {
    this.variablesList.push(this.createVariable());
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
    this.snackBar.open(this.errorMessage, 'OK');
  }

  public removeVariable(idx: number): void {
    const id = this.variablesList.controls[idx].get('id').value;
    if (id != null) {
      this.variablesToDelete.push(id);
    }
    this.variablesList.removeAt(idx);
  }
}
