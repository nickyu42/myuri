import { expect } from 'chai';
import 'mocha';

import { dummy } from '../api';

describe('Dummy function', () => {

  it('should return a number', () => {
    const result = dummy();
    expect(result).to.equal(42);
  });

});