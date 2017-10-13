import {Component, OnInit} from '@angular/core';
import {TemplatesApi} from "../../api/api/TemplatesApi";
import {Template} from "../../api/model/Template";

@Component({
  selector: 'app-templates',
  templateUrl: './templates.component.html',
  styleUrls: ['./templates.component.css'],
  providers: [TemplatesApi]
})
export class TemplatesComponent implements OnInit {
  public templates: Template[];
  public templatesVisible: boolean[] = [];

  constructor(private api: TemplatesApi) {
  }

  ngOnInit() {
    this.api.getTemplates().subscribe(d => {
      console.debug(d);
      this.templates = d;
      this.templates.forEach(value => this.templatesVisible[value.id] = false);
    });
  }

}
