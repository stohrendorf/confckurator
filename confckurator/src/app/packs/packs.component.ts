import {Component, Input, OnInit, Output} from '@angular/core';
import {PacksApi} from "../../api/api/PacksApi";
import {Pack} from "../../api/model/Pack";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-packs',
  templateUrl: './packs.component.html',
  styleUrls: ['./packs.component.css'],
  providers: [PacksApi]
})
export class PacksComponent implements OnInit {
  @Output()
  public packs: Pack[];

  @Output()
  public selectedPack?: Pack = null;

  @Input()
  @Output()
  public editingName: string = null;

  public nameDlgTitle: string;

  @Output()
  public errorMessage?: string = null;

  constructor(private api: PacksApi, private modalService: NgbModal) {
  }

  ngOnInit() {
    this.loadPacks();
  }

  public openRenameDlg(content) {
    const idx = this.packs.findIndex(e => e === this.selectedPack);
    this.editingName = this.packs[idx].name;
    this.nameDlgTitle = 'Rename Pack';
    this.modalService.open(content).result.then(reason => this.packs[idx].name = this.editingName, () => {
    });
  }

  public openNewDlg(content) {
    this.editingName = '';
    this.nameDlgTitle = 'New Pack';
    this.modalService.open(content).result.then(reason => {
      this.api.createPack({name: this.editingName})
        .subscribe(d => this.loadPacks(d.id), this.onError);
    }, () => {
    });
  }

  public openDeleteDlg(content) {
    this.modalService.open(content).result.then(reason => {
      this.api.deletePack(this.selectedPack.id).subscribe(x => this.loadPacks(), this.onError);
    }, () => {
    });
  }

  setSelectedPack(event) {
    this.selectedPack = event;
  }

  private loadPacks(id: number = null): void {
    this.api.getPacks().subscribe(data => {
      this.packs = data;
      this.selectedPack = null;
      if (this.packs.length > 0) {
        if (id != null) {
          for (const tpl of this.packs) {
            if (tpl.id === id) {
              this.selectedPack = tpl;
              break;
            }
          }
        }

        if (this.selectedPack == null) {
          this.selectedPack = this.packs[0];
        }
      }
    }, this.onError);
  }

  private onError(e): void {
    this.errorMessage = 'Sorry, an arbitrary kitten exploded.';
    this.errorMessage = e.json().message;
  }
}
