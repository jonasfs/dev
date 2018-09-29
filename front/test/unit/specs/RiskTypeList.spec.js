import Vue from 'vue';
import { shallowMount } from '@vue/test-utils'
import RiskTypeList from '@/components/RiskTypeList';

function mockFetch(data) {
  return jest.fn().mockImplementation(() =>
    Promise.resolve({
      ok: true,
      json: () => data
    })
  );
}


describe('RiskTypeList.vue', () => {
  it('should render correct contents', () => {
		window.fetch = mockFetch([{
			"id": 1,
			"name": "House",
			"fields": {
				"first_owner": "[\"yes\",\"no\"]",
				"purchased_in": "date",
				"price": "number",
				"owner": "text"
			}
		}]);
		const wrapper = shallowMount(RiskTypeList);
		expect(wrapper.isVueInstance()).toBeTruthy();
  });
});
