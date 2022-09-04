/* stores.js: global reactive states */

import { writable } from 'svelte/store';

// Get the system timezone and set it as the
// default timezone for the timezone state
const timezone = writable((new Date()).getTimezoneOffset());

export { timezone };

