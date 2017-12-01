import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {PacksComponent} from './packs/packs.component';
import {TemplatesComponent} from './templates/templates.component';
import {HttpModule} from '@angular/http';
import {BASE_PATH} from '../api';
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
import {NgxDatatableModule} from "@swimlane/ngx-datatable";
import {MatButtonModule, MatCardModule, MatFormFieldModule, MatInputModule, MatSnackBarModule} from "@angular/material";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

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
    BrowserAnimationsModule,
    RouterModule.forRoot(appRoutes, {useHash: true}),
    BrowserModule,
    HttpModule,
    ReactiveFormsModule,
    CodemirrorModule,
    FormsModule,
    NbThemeModule.forRoot({ name: 'default' }),
    NbLayoutModule,
    NbSidebarModule,
    NbMenuModule,
    NbActionsModule,
    NgxDatatableModule,
    MatCardModule,
    MatSnackBarModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule
  ],
  providers: [
    {provide: BASE_PATH, useValue: '/api'},
    {provide: APP_BASE_HREF, useValue: '/'},
    NbSidebarService,
    NbMenuService,
    NbMenuInternalService
    ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
