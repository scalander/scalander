<script>
    //chrono
    import * as chrono from 'chrono-node';
    import { format } from 'date-fns'
    //do format("yyyy-MM-dd HH:mm:ss")
    //

    // page info and svelte tooling
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    // our own UI components
    // import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"
    import Button from '$lib/components/ui/Button.svelte';

    // strings
    import strings from "$lib/strings.json";
    import { exclude_internal_props } from 'svelte/internal';
    import { parseISO } from 'date-fns';

    let name;
    let start;
    let end;
    let users; //stores emails separated by commas
    let lockIn;
    let meeting = {"name": "", "start": "", "end": "", "users": "", "lockIn": ""};

    
    // puts meeting info into one object
    function meetingAppend(items){
        // console.log(typeof item)
        for (let i = 0; i < items.length; i++){
            let key = Object.keys(items[i]);
            let item = items[i];
            meeting[key] = item[key];
        }
    }
</script>


<div id="page-container">
    <div id="create-form">
        <h1>{strings.CREATE_A_MEETING}</h1>
        <form class = "meeting-form"> <!-- TODO: make a thing for input fields bc listing all of them here is hella messy -->
            <h2 class="meeting-subhead">{strings.MEETING_NAME}</h2>
            <input type="text"
                   placeholder="{strings.MEETING_NAME_PLACEHOLDER}"
                   bind:value={name} />

            <h2 class="meeting-subhead">{strings.MEETING_START}</h2>
            <input type="text" bind:value={start} />

            <h2 class="meeting-subhead">{strings.MEETING_END}</h2>
            <input type="text" bind:value={end} />

            <h2 class="meeting-subhead">{strings.MEETING_LOCK_IN}</h2>
            <input type="text" bind:value={lockIn} />
        </form>
        <div id="submit">
            <Button primary>{strings.MEETING_SUBMIT}</Button>
        </div>
    </div>
</div>


<style>
    #page-container{
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    h1 {
        font-weight: 700;
        color: var(--accent);
        font-size: 30px;
    }

    .meeting-subhead {
        color: var(--secondary);
        font-size: 13px;
        font-weight: 600;
    }

    input {
        margin-bottom: 15px;
        font-size: 15px;
        padding: 5px;
        margin: 5px 0;
        max-width: 600px;
        width: min(90vw, 600px);
        border: 1px solid transparent;
        border-radius: 5px;
        transition: border-color 0.2s linear;
    }

    input:hover {
        border: 1px solid var(--tertiary);
    }

    input:focus {
        border: 1px solid var(--accent);
        outline: 0;
    }

    #submit {
        margin-top: 20px;
    }

</style>
