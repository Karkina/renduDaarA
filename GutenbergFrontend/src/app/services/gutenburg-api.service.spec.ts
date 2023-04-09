import { TestBed } from '@angular/core/testing';

import { GutenburgAPIService } from './gutenburg-api.service';

describe('GutenburgAPIService', () => {
  let service: GutenburgAPIService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GutenburgAPIService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
