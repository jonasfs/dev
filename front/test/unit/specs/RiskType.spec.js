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
		"fields": [
			{
				"id": 1,
				"name": "country",
				"field_type": ["Brazil", "Mexico", "USA", "Canada"],
			},
			{
				"id": 2,
				"name": "owner",
				"field_type": "TextField",
			},
			{
				"id": 3,
				"name": "value",
				"field_type": "NumberField",
			},
			{
				"id": 4,
				"name": "expires",
				"field_type": "DateField",
			},
		],
	};

	it('should render contents correctly', () => {
		const wrapper = shallowMount(RiskType, {
			propsData: {
				risk: riskProps,
			},
		});
		expect(wrapper.isVueInstance()).toBeTruthy();
		expect(wrapper.findAll('input').length).toEqual(3);
		expect(wrapper.vm.getValue('owner')).toEqual('');
		expect(wrapper.vm.getValue('country')).toEqual('');
		expect(wrapper.vm.getValue('value')).toEqual('');
		expect(wrapper.vm.getValue('expires')).toEqual('');
	});

	it('should update input properly', () => {
		const wrapper = shallowMount(RiskType, {
			propsData: {
				risk: riskProps,
			},
		});
		const input = wrapper.find('input[type="text"]');
		input.setValue('Foo Bar');
		expect(wrapper.vm.getValue('owner')).toEqual('Foo Bar');
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

	it('getFieldType for indeterminate field should return null', () => {
		const wrapper = shallowMount(RiskType, {
			propsData: {
				risk: riskProps,
			},
		});
		expect(
			wrapper.vm.getFieldType(wrapper.vm.fields[0]['field_type'])
		).toEqual(null);

	});
});
