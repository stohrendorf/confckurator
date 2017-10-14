import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {PacksComponent} from './packs/packs.component';
import {TemplatesComponent} from './templates/templates.component';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {HttpModule} from '@angular/http';
import {BASE_PATH} from '../api/variables';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CodemirrorModule} from 'ng2-codemirror';

@NgModule({
  declarations: [
    AppComponent,
    PacksComponent,
    TemplatesComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    NgbModule.forRoot(),
    ReactiveFormsModule,
    CodemirrorModule,
    FormsModule
  ],
  providers: [{provide: BASE_PATH, useValue: '/api'}],
  bootstrap: [AppComponent]
})
export class AppModule {
}
