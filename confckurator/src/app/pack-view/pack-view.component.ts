import {Component, Input, OnInit, Output} from '@angular/core';
import {FormArray, FormBuilder, FormGroup} from '@angular/forms';
import {PacksApi} from '../../api/api/PacksApi';
import {Pack} from '../../api/model/Pack';
import {Instance} from '../../api/model/Instance';
import {MatSnackBar} from "@angular/material";

@Component({
  selector: 'app-pack-view',
  templateUrl: './pack-view.component.html',
  styleUrls: ['./pack-view.component.css'],
  providers: [FormBuilder, PacksApi]
})
export class PackViewComponent implements OnInit {
  public instanceForm: FormGroup;
  public instanceList: FormArray;

  @Output()
  public errorMessage?: string = null;

  private instancesToDelete: number[] = [];

  private activePack: Pack;

  constructor(private api: PacksApi, private formBuilder: FormBuilder, private snackBar: MatSnackBar) {
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
    this.instanceList = this.formBuilder.array([]);
    this.instanceForm = this.formBuilder.group({
      instances: this.instanceList
    });
  }

  public createInstance(instance: Instance = null): FormGroup {
    return this.formBuilder.group({
      name: [!instance ? '' : instance.name],
      id: [!instance ? null : instance.id],
      template_id: [!instance ? null : instance.template_id],
      template_name: [!instance ? '' : instance.template_name]
    });
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
    this.instanceList.push(this.createInstance());
  }

  public removeInstance(idx: number): void {
    const id = this.instanceList.controls[idx].get('id').value;
    if (id != null) {
      this.instancesToDelete.push(id);
    }
    this.instanceList.removeAt(idx);
  }

  private load(): void {
    if (this.activePack == null || this.activePack.id == null) {
      return;
    }

    this.api.getPack(this.activePack.id).subscribe(t => {
      this.activePack.name = t.name;
      this.activePack.name = t.name;
      this.activePack.instances = t.instances;
      this.updateDisplay();
    }, this.onError);
  }

  private updateDisplay(): void {
    while (this.instanceList.length > 0) {
      this.instanceList.removeAt(0);
    }

    this.activePack.instances.forEach(v => {
      this.instanceList.push(this.createInstance(v));
    });
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
    this.snackBar.open(this.errorMessage, 'OK');
  }
}
