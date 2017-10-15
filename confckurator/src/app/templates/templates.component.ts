import {Component, OnInit, Output} from '@angular/core';
import {TemplatesApi} from '../../api/api/TemplatesApi';
import {Template} from '../../api/model/Template';
import {AbstractControl, FormArray, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Variable} from '../../api/model/Variable';
import 'codemirror/mode/jinja2/jinja2';
import 'codemirror/mode/dockerfile/dockerfile';
import 'codemirror/addon/dialog/dialog';
import 'codemirror/addon/search/match-highlighter';
import 'codemirror/addon/search/searchcursor';
import 'codemirror/addon/search/search';
import 'codemirror/addon/edit/matchbrackets';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/observable/forkJoin';
import {List} from 'linqts';
import {IdResponse} from '../../api/model/IdResponse';

class TemplateInfo {
  public variablesForm: FormGroup;
  public variablesList: FormArray;
  public code = '';

  public errorMessage?: string = null;

  private variablesToDelete: number[] = [];

  constructor(private api: TemplatesApi, private formBuilder: FormBuilder, private template: Template) {
    this.reload();
  }

  reload(): void {
    if (!this.variablesList) {
      this.variablesList = this.formBuilder.array([]);
      this.variablesForm = this.formBuilder.group({
        variables: this.variablesList
      });
    }

    this.api.getTemplate(this.template.id, true).subscribe(t => {
      this.template = t;
      this.updateDisplay();
    }, e => this.errorMessage = e.json().message);
  }

  createVariable(variable: Variable = null): FormGroup {
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
        this.doUpdate();
      }, e => this.errorMessage = e.json().message);
    } else {
      this.doUpdate();
    }
  }

  private doUpdate(): Observable<IdResponse> {
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

    request.subscribe(x => this.reload(), e => {
      this.errorMessage = e.json().message;
      this.reload();
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

@Component({
  selector: 'app-templates',
  templateUrl: './templates.component.html',
  styleUrls: [
    './templates.component.css'
  ],
  providers: [FormBuilder, TemplatesApi]
})
export class TemplatesComponent implements OnInit {
  public infos: TemplateInfo[] = [];

  constructor(private formBuilder: FormBuilder, private api: TemplatesApi) {
  }

  ngOnInit() {
    this.api.getTemplates().subscribe(data => {
      data.forEach(v => this.infos.push(new TemplateInfo(this.api, this.formBuilder, v)));
    });
  }
}
