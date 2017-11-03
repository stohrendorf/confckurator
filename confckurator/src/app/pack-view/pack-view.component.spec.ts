import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {PackViewComponent} from './pack-view.component';

describe('PackViewComponent', () => {
  let component: PackViewComponent;
  let fixture: ComponentFixture<PackViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PackViewComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PackViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
