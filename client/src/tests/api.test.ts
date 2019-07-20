import dummy from '../api';

import { expect } from 'chai';
import 'mocha';

describe('Dummy function', () => {

  it('should return a number', () => {
    const result = dummy();
    expect(result).to.equal(42);
  });

});