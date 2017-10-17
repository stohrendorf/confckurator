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
  private static readonly templateTemplate = 'template={{_meta.template}};\nenvironment={{_meta.environment}};\npack={{_meta.pack}}';

  @Output()
  public templates: Template[];

  @Output()
  public selectedTemplate?: Template = null;

  @Input()
  @Output()
  public editingName: string = null;

  public nameDlgTitle: string;

  @Output()
  public errorMessage?: string = null;

  constructor(private api: TemplatesApi, private modalService: NgbModal) {
  }

  ngOnInit() {
    this.loadTemplates();
  }

  private loadTemplates(id: number = null): void {
    this.api.getTemplates().subscribe(data => {
      this.templates = data;
      this.selectedTemplate = null;
      if (this.templates.length > 0) {
        if (id != null) {
          for (const tpl of this.templates) {
            if (tpl.id === id) {
              this.selectedTemplate = tpl;
              break;
            }
          }
        }

        if (this.selectedTemplate == null) {
          this.selectedTemplate = this.templates[0];
        }
      }
    }, this.onError);
  }

  public openRenameDlg(content) {
    const idx = this.templates.findIndex(e => e === this.selectedTemplate);
    this.editingName = this.templates[idx].name;
    this.nameDlgTitle = 'Rename Template';
    this.modalService.open(content).result.then(reason => this.templates[idx].name = this.editingName, () => {
    });
  }

  public openNewDlg(content) {
    this.editingName = '';
    this.nameDlgTitle = 'New Template';
    this.modalService.open(content).result.then(reason => {
      this.api.createTemplate({name: this.editingName, text: TemplatesComponent.templateTemplate})
        .subscribe(d => this.loadTemplates(d.id), this.onError);
    }, () => {
    });
  }

  public openDeleteDlg(content) {
    this.modalService.open(content).result.then(reason => {
      this.api.deleteTemplate(this.selectedTemplate.id).subscribe(x => this.loadTemplates(), this.onError);
    }, () => {
    });
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
  }
}
