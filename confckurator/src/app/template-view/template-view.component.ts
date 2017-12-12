import {Component, Input, OnInit, Output} from '@angular/core';
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
  providers: [TemplatesApi]
})
export class TemplateViewComponent implements OnInit {
  public code = '';

  @Output()
  public errorMessage?: string = null;

  private variablesToDelete: number[] = [];

  private activeTemplate: Template;

  constructor(private api: TemplatesApi, private snackBar: MatSnackBar) {
  }

  ngOnInit() {
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

  public createVariable(variable: Variable = null): Variable {
    if (variable != null) {
      this.activeTemplate.variables.push(variable);
      return variable;
    }
    else {
      let v: Variable = {
        name: '',
        in_use: false,
        description: '',
        id: null
      };
      this.activeTemplate.variables.push(v);
      return v;
    }
  }

  private updateDisplay(): void {
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
          create: new List<Variable>(this.activeTemplate.variables)
            .Where(c => c.id == null)
            .Select(c => {
              return {
                name: c.name,
                description: c.description
              };
            })
            .ToArray(),
          delete: this.variablesToDelete,
          update: new List<Variable>(this.activeTemplate.variables)
            .Where(c => c.id != null)
            .Select(c => {
              return {
                id: c.id,
                description: c.description,
                name: c.name
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
    this.createVariable();
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
    this.snackBar.open(this.errorMessage, 'OK');
  }

  public removeVariable(idx: number): void {
    const id = this.activeTemplate.variables[idx].id;
    if (id != null) {
      this.variablesToDelete.push(id);
    }
    delete this.activeTemplate.variables[idx];
  }
}
