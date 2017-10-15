import {Component, OnInit} from '@angular/core';
import {TemplatesApi} from '../../api/api/TemplatesApi';
import 'codemirror/mode/jinja2/jinja2';
import 'codemirror/mode/dockerfile/dockerfile';
import 'codemirror/addon/dialog/dialog';
import 'codemirror/addon/search/match-highlighter';
import 'codemirror/addon/search/searchcursor';
import 'codemirror/addon/search/search';
import 'codemirror/addon/edit/matchbrackets';
import 'rxjs/add/observable/forkJoin';
import {Template} from '../../api/model/Template';

@Component({
  selector: 'app-templates',
  templateUrl: './templates.component.html',
  styleUrls: ['./templates.component.css'],
  providers: [TemplatesApi]
})
export class TemplatesComponent implements OnInit {
  templates: Template[];

  constructor(private api: TemplatesApi) {
  }

  ngOnInit() {
    this.api.getTemplates().subscribe(data => this.templates = data);
  }
}
