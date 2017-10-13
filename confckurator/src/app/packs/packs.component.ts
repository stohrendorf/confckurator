import {Component, OnInit} from '@angular/core';
import {PacksApi} from "../../api/api/PacksApi";
import {Pack} from "../../api/model/Pack";

@Component({
  selector: 'app-packs',
  templateUrl: './packs.component.html',
  styleUrls: ['./packs.component.css'],
  providers: [PacksApi]
})
export class PacksComponent implements OnInit {
  packs: Pack[];

  constructor(private api: PacksApi) {
  }

  ngOnInit() {
    this.api.getPacks().subscribe(d => {
      console.debug(d);
      this.packs = d;
    });
  }
}
