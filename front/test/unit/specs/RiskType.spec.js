/*
 * RiskType.spec.js
 * Copyright (C) 2018 jonasfscc <jonasfscc@gmail.com>
 *
 */

import Vue from 'vue'
import {shallowMount} from '@vue/test-utils'
import RiskType from '@/components/RiskType'

describe('RiskType.vue', () => {
	const riskProps = {
		"id": 1,
		"name": "Prize",
		"fields": {
			"country": "[\"Brazil\",\"Mexico\",\"USA\",\"Canada\"]",
			"owner": "text",
			"value": "number",
			"expires": "date"
		}
	};

	it('should render contents correctly', () => {
		const wrapper = shallowMount(RiskType, {
			propsData: {
				risk: riskProps,
			},
		});
		expect(wrapper.isVueInstance()).toBeTruthy();
		expect(wrapper.findAll('input').length).toEqual(3);
		expect(wrapper.vm.values).toEqual({
			country: '',
			owner: '',
			value: '',
			expires: ''
		});
	});

	it('should update input properly', () => {
		const wrapper = shallowMount(RiskType, {
			propsData: {
				risk: riskProps,
			},
		});
		const input = wrapper.find('input[type="text"]');
		input.setValue('Foo Bar');
		expect(wrapper.vm.values.owner).toEqual('Foo Bar');
	});

	it('number field should keep empty state when input is non-numeric ', () => {
		const wrapper = shallowMount(RiskType, {
			propsData: {
				risk: riskProps,
			},
		});
		const input = wrapper.find('input[type="number"]');
		input.setValue('Foo Bar');
		expect(wrapper.vm.values.value).toEqual('');
	});
});
