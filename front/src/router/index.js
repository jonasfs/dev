import Vue from 'vue';
import Router from 'vue-router';
import RiskTypeList from '@/components/RiskTypeList';

Vue.use(Router);

export default new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			name: 'RiskTypeList',
			component: RiskTypeList,
		},
	],
});
