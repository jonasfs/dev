<!--
	TextInput.vue
	Copyright (C) 2018 jonasfscc <jonasfscc@gmail.com>
-->

<script>
export default {
	name: 'EnumInput',
	props: {
		name: String,
		initialValue: String,
		choices: Array,
	},
	data() {
		return {
			choiceList: [],
			value: '',
		};
	},
	created() {
		this.choiceList = this.choices;
		this.value = this.initialValue;
	},
	methods: {
		changeSelect(newValue) {
			this.$emit('changeSelect', this.name, newValue);
		},
	},
};
</script>

<template>
	<div class="select">
		<select v-model="value" v-on:change="changeSelect(value)">
			<option
				value=""
				:selected="value === ''? true : false"
			>
				-- select --
			</option>
			<option
				v-for="(choice, index) in choiceList"
				:key="index"
				:selected="value === choice? true : false"
			>
				{{choice}}
			</option>
		</select>
	</div>
</template>

<style scoped>
</style>
