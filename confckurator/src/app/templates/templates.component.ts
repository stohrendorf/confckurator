import {Component, OnInit} from '@angular/core';
import {TemplatesApi} from '../../api/api/TemplatesApi';
import {Template} from '../../api/model/Template';
import {FormArray, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Variable} from '../../api/model/Variable';
import 'codemirror/mode/jinja2/jinja2';

class TemplateInfo {
  public variablesForm: FormGroup;
  public variablesList: FormArray;
  public code = '';

  constructor(api: TemplatesApi, private formBuilder: FormBuilder, public template: Template) {
    this.variablesList = this.formBuilder.array([]);
    this.variablesForm = this.formBuilder.group({
      variables: this.variablesList
    });

    this.template.variables.forEach(v => {
      this.variablesList.push(this.createAddress(v));
    });

    api.getTemplate(this.template.id, true).subscribe(t => this.code = t.text);
  }

  createAddress(variable: Variable = null): FormGroup {
    return this.formBuilder.group({
      name: [
        {value: !variable ? '' : variable.name, disabled: variable != null},
        Validators.pattern(/^[a-zA-Z_][a-zA-Z0-9_]*$/)
      ],
      description: [!variable ? '' : variable.description],
      id: [!variable ? -1 : variable.id]
    });
  }

  addVariable(): void {
    this.variablesList.push(this.createAddress());
  }

  removeVariable(idx: number): void {
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
