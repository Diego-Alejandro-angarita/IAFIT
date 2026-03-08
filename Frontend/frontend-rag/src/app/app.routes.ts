import { Routes } from '@angular/router';
import { HomePage } from './pages/home/home.page';
import { ModulePage } from './pages/module/module.page';

export const routes: Routes = [
	{
		path: '',
		component: HomePage
	},
	{
		path: 'map',
		component: ModulePage,
		data: { moduleKey: 'map' }
	},
	{
		path: 'classrooms',
		component: ModulePage,
		data: { moduleKey: 'classrooms' }
	},
	{
		path: 'restaurants',
		component: ModulePage,
		data: { moduleKey: 'restaurants' }
	},
	{
		path: 'events',
		component: ModulePage,
		data: { moduleKey: 'events' }
	},
	{
		path: 'calendar',
		component: ModulePage,
		data: { moduleKey: 'calendar' }
	},
	{
		path: 'directory',
		component: ModulePage,
		data: { moduleKey: 'directory' }
	},
	{
		path: 'groups',
		component: ModulePage,
		data: { moduleKey: 'groups' }
	},
	{
		path: 'profile',
		component: ModulePage,
		data: { moduleKey: 'profile' }
	},
	{
		path: 'chat',
		component: ModulePage,
		data: { moduleKey: 'chat' }
	},
	{
		path: '**',
		redirectTo: ''
	}
];
