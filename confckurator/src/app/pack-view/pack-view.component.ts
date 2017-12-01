import {Component, Input, OnInit, Output} from '@angular/core';
import {PacksApi} from '../../api';
import {Pack} from '../../api';
import {MatSnackBar} from "@angular/material";

@Component({
  selector: 'app-pack-view',
  templateUrl: './pack-view.component.html',
  styleUrls: ['./pack-view.component.css'],
  providers: [PacksApi]
})
export class PackViewComponent implements OnInit {
  @Output()
  public errorMessage?: string = null;

  private instancesToDelete: number[] = [];

  private activePack: Pack;

  constructor(private api: PacksApi, private snackBar: MatSnackBar) {
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
