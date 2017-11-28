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
import {TemplateViewComponent} from './template-view/template-view.component';
import {EnvironmentsListComponent} from './environmentslist/environmentslist.component';
import {PackViewComponent} from './pack-view/pack-view.component';
import {
  NbActionsModule,
  NbLayoutModule, NbMenuModule, NbMenuService, NbSidebarModule, NbSidebarService,
  NbThemeModule
} from "@nebular/theme";
import {RouterModule, Routes} from "@angular/router";
import {APP_BASE_HREF} from "@angular/common";
import {NbMenuInternalService} from "@nebular/theme/components/menu/menu.service";

const appRoutes: Routes = [
  {path: 'packs', component: PacksComponent},
  {path: 'templates', component: TemplatesComponent},
  {path: 'environments', component: EnvironmentsListComponent},
  {path: '', redirectTo: '/packs', pathMatch: 'full'}
];

@NgModule({
  declarations: [
    AppComponent,
    PacksComponent,
    TemplatesComponent,
    TemplateViewComponent,
    EnvironmentsListComponent,
    PackViewComponent
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    HttpModule,
    NgbModule.forRoot(),
    ReactiveFormsModule,
    CodemirrorModule,
    FormsModule,
    NbThemeModule.forRoot({ name: 'default' }),
    NbLayoutModule,
    NbSidebarModule,
    NbMenuModule,
    NbActionsModule
  ],
  providers: [
    {provide: BASE_PATH, useValue: '/api'},
    {provide: APP_BASE_HREF, useValue: '/static/frontend'},
    NbSidebarService,
    NbMenuService,
    NbMenuInternalService
    ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
