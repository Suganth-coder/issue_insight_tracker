/// <reference types="svelte-clerk/env" />

import type { AuthObject } from '@clerk/backend';

declare global {
	namespace App {
		interface Locals {
			auth: () => AuthObject;
		}
	}
}
