/*
 * EnumInput.spec.js
 * Copyright (C) 2018 jonasfscc <jonasfscc@gmail.com>
 *
 */

import Vue from 'vue'
import { shallowMount } from '@vue/test-utils'
import EnumInput from '@/components/EnumInput'

describe('EnumInput.vue', () => {
	it('should render contents correctly', () => {
		const wrapper = shallowMount(EnumInput, {
			propsData: {
				name: 'first_owner',
				initialValue: '',
				choices: ["yes","no"]
			}
		});
		expect(wrapper.isVueInstance()).toBeTruthy();
		expect(wrapper.find('select').exists()).toBe(true);
		expect(wrapper.findAll('option').length).toEqual(3);
	});

	it('check if state is updated correctly', () => {
		const wrapper = shallowMount(EnumInput, {
			propsData: {
				name: 'first_owner',
				initialValue: '',
				choices: ["yes","no"]
			}
		});
		expect(wrapper.vm.choiceList).toEqual(["yes", "no"]);
		expect(wrapper.vm.value).toEqual("");
		const options = wrapper.find('select').findAll('option');
		options.at(1).setSelected();
		expect(wrapper.emitted().changeSelect).toBeTruthy();
		expect(wrapper.vm.value).toEqual("yes");
	});
});

