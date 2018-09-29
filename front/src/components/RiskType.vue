<!--
	RiskType.vue
	Copyright (C) 2018 jonasfscc <jonasfscc@gmail.com>
-->

<script>
import EnumInput from '@/components/EnumInput';

export default {
	name: 'RiskType',
	props: {
		risk: Object,
	},
	data() {
		return {
			fields: [],
			values: {},
		};
	},
	components: {
		EnumInput,
	},
	created() {
		this.fields = this.risk.fields;
		Object.keys(this.fields).forEach((key) => {
			this.values[key] = '';
		});
	},
	methods: {
		getValue(name) {
			return this.values[name];
		},
		setValue(name, value) {
			this.values[name] = value;
		},
	},
};
</script>

<template>
	<div>
		<form>
			<div class="field">
				<label class="label is-large has-text-primary">
					{{risk.name}}
				</label>
			</div>
			<div
				class="field"
				v-for="(type, name, index) in fields"
				:key="index"
			>
				<div class="field">
					<label class="label">
						{{name}}
						<span v-if="
							(type === 'number' || type === 'text') || type === 'date'"
						>
							({{type}})
						</span>
						<span v-else>
							(enum: {{type}})
						</span>
					</label>
					<div class="control">
						<template v-if="
							(type === 'number' || type === 'text') || type === 'date'"
						>
							<input
								class="input"
								:type="type"
								:value="getValue(name)"
								@input="setValue(name, $event.target.value)"
							>
						</template>
						<template v-else>
							<EnumInput
								:name="name"
								:choices="type"
								:initialValue="getValue(name)"
								@changeSelect="setValue"
							>
							</EnumInput>
						</template>
					</div>
				</div>
			</div>
			<hr/>
		</form>
	</div>
</template>

<style scoped>
</style>
