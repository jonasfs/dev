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
		this.fields.forEach((field) => {
			this.values[field.name] = '';
		});
	},
	methods: {
		getFieldType(fieldType) {
			if (fieldType === 'NumberField') {
				return 'number';
			} else if (fieldType === 'TextField') {
				return 'text';
			} else if (fieldType === 'DateField') {
				return 'date';
			}
			return null;
		},
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
				v-for="(field, index) in fields"
				:key="index"
			>
				<div class="field">
					<label class="label">
						{{field.name}}
						<span v-if="
							(field.field_type === 'NumberField' || field.field_type === 'TextField')
								|| field.field_type === 'DateField'
							"
						>
							({{field.field_type}})
						</span>
						<span v-else>
							(enum: {{field.choices}})
						</span>
					</label>
					<div class="control">
						<template
							v-if="
								(
									field.field_type === 'NumberField'
										|| field.field_type === 'TextField'
								)
									|| field.field_type === 'DateField'
							"
						>
							<input
								class="input"
								:type="getFieldType(field.field_type)"
								:value="getValue(field.name)"
								@input="setValue(field.name, $event.target.value)"
							>
						</template>
						<template v-else>
							<EnumInput
								:name="field.name"
								:choices="field.choices"
								:initialValue="getValue(field.name)"
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
