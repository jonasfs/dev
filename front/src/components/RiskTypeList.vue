<!--
	RiskTypeList.vue
	Copyright (C) 2018 jonasfscc <jonasfscc@gmail.com>
-->

<script>
import RiskType from '@/components/RiskType';

export default {
	name: 'RiskTypeList',
	data() {
		return {
			list: [],
		};
	},
	created() {
		let url = process.env.ROOT_API;
		url += 'risktypes/';
		const ref = this;
		fetch(url)
			.then(resp => resp.json())
			.then((json) => {
				ref.list = json;
			});
	},
	components: {
		RiskType,
	},
};
</script>

<template>
	<section class="section">
		<div class="container">
			<div class="columns">
				<div class="column">
				</div>
				<div class="column is-10">
					<ul>
						<li v-for="risk in list" v-bind:key="risk.id">
							<RiskType
								v-bind:risk="risk"
							/>
						</li>
					</ul>
				</div>
				<div class="column">
				</div>
			</div>
		</div>
	</section>
</template>


<style scoped>
</style>
