import {Component, Input, OnInit, Output} from '@angular/core';
import {Environment, EnvironmentsApi, PacksApi, Template, TemplatesApi} from '../../api';
import {Pack} from '../../api';
import {MatSnackBar} from "@angular/material";

@Component({
  selector: 'app-pack-view',
  templateUrl: './pack-view.component.html',
  styleUrls: ['./pack-view.component.css'],
  providers: [PacksApi, TemplatesApi, EnvironmentsApi]
})
export class PackViewComponent implements OnInit {
  @Output()
  public errorMessage?: string = null;

  private instancesToDelete: number[] = [];

  private activePack: Pack;

  public templates: Template[];

  public environments: Environment[];

  constructor(private api: PacksApi, private templateApi: TemplatesApi, private environmentsApi: EnvironmentsApi, private snackBar: MatSnackBar) {
  }

  public get pack(): Pack {
    return this.activePack;
  }

  @Input()
  public set pack(tpl: Pack) {
    this.activePack = tpl;
    this.load();
  }

  ngOnInit() {
    this.templateApi.getTemplates().subscribe(
      tpls => this.templates = tpls,
      this.onError
    );
    this.environmentsApi.getEnvironments().subscribe(
      envs => this.environments = envs,
      this.onError
    );
  }

  public save(): void {
    if (this.activePack.id == null) {
      this.api.createPack({name: this.activePack.name}).subscribe(pack => {
        this.activePack.id = pack.id;
        // this.sendSaveRequest();
      }, this.onError);
    } else {
      // this.sendSaveRequest();
    }
  }

  public addInstance(): void {
    this.activePack.instances.push({id: null, name: '', template_id: null, template_name: '', values: []});
  }

  public removeInstance(idx: number): void {
    const id = this.activePack.instances[idx].id;
    if (id != null) {
      this.instancesToDelete.push(id);
    }
    delete this.activePack.instances[idx];
  }

  private load(): void {
    if (this.activePack == null || this.activePack.id == null) {
      return;
    }

    this.api.getPack(this.activePack.id).subscribe(t => {
      this.activePack.name = t.name;
      this.activePack.name = t.name;
      this.activePack.instances = t.instances;
    }, this.onError);
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
    this.snackBar.open(this.errorMessage, 'OK');
  }
}
