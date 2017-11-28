import {Component} from '@angular/core';
import {NbMenuItem} from "@nebular/theme";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  public menuItems: NbMenuItem[] = [
    {title: 'Packs', link: '/packs'},
    {title: 'Environments', link: '/environments'},
    {title: 'Templates', link: '/templates'}
  ];
}
