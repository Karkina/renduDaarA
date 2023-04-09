import { TestBed } from '@angular/core/testing';

import { ApiCallServiceService } from './api-call-service.service';

describe('ApiCallServiceService', () => {
  let service: ApiCallServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ApiCallServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
