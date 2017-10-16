import {Component, Input, OnInit} from '@angular/core';
import {AbstractControl, FormArray, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {TemplatesApi} from '../../api/api/TemplatesApi';
import {Template} from '../../api/model/Template';
import {Variable} from '../../api/model/Variable';
import {Observable} from 'rxjs/Observable';
import {IdResponse} from '../../api/model/IdResponse';
import {List} from 'linqts';

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

  public errorMessage?: string = null;

  private variablesToDelete: number[] = [];

  private template: Template;

  constructor(private api: TemplatesApi, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
    this.variablesList = this.formBuilder.array([]);
    this.variablesForm = this.formBuilder.group({
      variables: this.variablesList
    });
  }

  @Input()
  public set templateId(id: number) {
    this.load(id);
  }

  private load(id: number): void {
    if (id == null) {
      return;
    }

    this.api.getTemplate(id, true).subscribe(t => {
      this.template = t;
      this.updateDisplay();
    }, e => this.errorMessage = e.json().message);
  }

  public createVariable(variable: Variable = null): FormGroup {
    return this.formBuilder.group({
      name: [
        {value: variable == null ? '' : variable.name, disabled: variable != null && variable.in_use},
        Validators.pattern(/^[a-zA-Z_][a-zA-Z0-9_]*$/)
      ],
      description: [!variable ? '' : variable.description],
      id: [!variable ? -1 : variable.id]
    });
  }

  private updateDisplay(): void {
    while (this.variablesList.length > 0) {
      this.variablesList.removeAt(0);
    }

    this.template.variables.forEach(v => {
      this.variablesList.push(this.createVariable(v));
    });

    this.code = this.template.text;
  }

  public save(): void {
    if (this.template.id < 0) {
      this.api.createTemplate({name: this.template.name, text: ''}).subscribe(tpl => {
        this.template.id = tpl.id;
        this.sendSaveRequest();
      }, e => this.errorMessage = e.json().message);
    } else {
      this.sendSaveRequest();
    }
  }

  private sendSaveRequest(): Observable<IdResponse> {
    const request = this.api
      .updateTemplate(this.template.id, {
        text: this.code,
        variables: {
          create: new List<AbstractControl>(this.variablesList.controls)
            .Where(c => c.get('id').value < 0)
            .Select(c => {
              return {
                name: c.get('name').value,
                description: c.get('description').value
              };
            })
            .ToArray(),
          delete: this.variablesToDelete,
          update: new List<AbstractControl>(this.variablesList.controls)
            .Where(c => c.get('id').value >= 0)
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

    request.subscribe(x => this.load(this.template.id), e => {
      this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
      this.errorMessage = e.json().message;
    });

    return request;
  }

  public addVariable(): void {
    this.variablesList.push(this.createVariable());
  }

  public removeVariable(idx: number): void {
    this.variablesToDelete.push(this.variablesList.controls[idx].get('id').value);
    this.variablesList.removeAt(idx);
  }
}
