import {Component, Input, OnInit, Output} from '@angular/core';
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
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-templates',
  templateUrl: './templates.component.html',
  styleUrls: ['./templates.component.css'],
  providers: [TemplatesApi]
})
export class TemplatesComponent implements OnInit {
  @Output()
  public templates: Template[];

  @Input()
  @Output()
  public selectedTemplate?: Template = null;

  @Input()
  @Output()
  public editingName: string = null;

  constructor(private api: TemplatesApi, private modalService: NgbModal) {
  }

  ngOnInit() {
    this.api.getTemplates().subscribe(data => {
      this.templates = data;
      if (this.templates.length > 0) {
        this.selectedTemplate = this.templates[0];
      }
    });
  }

  open(content) {
    const idx = this.templates.findIndex(e => e === this.selectedTemplate);
    this.editingName = this.templates[idx].name;
    this.modalService.open(content).result.then(reason => this.templates[idx].name = this.editingName);
  }
}
