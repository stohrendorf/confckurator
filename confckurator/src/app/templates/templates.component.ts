import {Component, OnInit} from '@angular/core';
import {TemplatesApi} from '../../api/api/TemplatesApi';
import {Template} from '../../api/model/Template';
import {FormArray, FormBuilder, FormGroup, Validators} from '@angular/forms';
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
import {IdResponse} from '../../api/model/IdResponse';

class TemplateInfo {
  public variablesForm: FormGroup;
  public variablesList: FormArray;
  public code = '';

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
    });
  }

  createVariable(variable: Variable = null): FormGroup {
    return this.formBuilder.group({
      name: [
        {value: !variable ? '' : variable.name, disabled: variable != null},
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
    let tplRequest: Observable<IdResponse>;
    if (this.template.id < 0) {
      tplRequest = this.api.createTemplate({name: this.template.name, text: this.code});
    } else {
      tplRequest = this.api.updateTemplate(this.template.id, {text: this.code});
    }

    tplRequest.subscribe(tpl => {
      this.template.id = tpl.id;
      const requests = this.saveVariables();
      if (requests.length > 0) {
        Observable.forkJoin(requests).subscribe(x => this.reload());
      } else {
        this.reload();
      }
    });
  }

  private saveVariables(): Observable<any>[] {
    let result: Observable<any>[] = this.variablesList.controls.map(vc => {
      const id: number = vc.get('id').value;
      const name: string = vc.get('name').value;
      const description: string = vc.get('description').value;

      if (id < 0) {
        return this.api.createTemplateVariable(this.template.id, {
          name: name,
          description: description
        });
      } else {
        return this.api.updateTemplateVariable(this.template.id, id, {
          description: description
        });
      }
    });

    result.push(
      ...this.variablesToDelete.map(id => this.api.deleteTemplateVariable(this.template.id, id))
    );

    this.variablesToDelete = [];

    return result;
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
