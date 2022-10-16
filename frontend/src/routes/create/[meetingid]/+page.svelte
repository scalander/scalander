<!-- <svelte:head>
    <script src="https://accounts.google.com/gsi/client" on:load={loadGoogle} />
</svelte:head> -->

<!-- base copied from ./schedule/[uid] -->
<script>
    //chrono
    import * as chrono from 'chrono-node';

    // page info and svelte tooling
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    // our own UI components
    import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"
    import Button from '$lib/components/ui/Button.svelte';

    // strings
    import strings from "$lib/strings.json";
    import { exclude_internal_props } from 'svelte/internal';
    import { parseISO } from 'date-fns';

    //state 0 (doen't exist yet) = begin meeting creation screen
    //state 1 = form
    //state 2 = confirmation screen (will probably come later)
    let state = 1
    let name
    let start
    let end
    let users = []
    let lockIn
    let meeting

    function submit(name, start, end, users, lockIn){ //name = string, start = datetime, end = datetime, users = [User], lockIn = datetime
        pass
    }

</script>


<div id="page-container">
    <div id="meeting-form">
        <!-- State 1 is the form -->
        {#if state==1}
            <h1>{strings.CREATE_A_MEETING}</h1>
            <form class = "meeting-form"> <!-- TODO: make a thing for input fields bc listing all of them here is hella messy -->
                <label for = "field-label">{strings.MEETING_NAME}</label>
                <input type = "text" bind:value={name} />
                <label for = "field-label">{strings.MEETING_START}</label>
                <input type = "text" bind:value={name} />
            </form>
        {/if}
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

   

    #meeting-form {
        display: grid;
        gap: 100px 200px;
        grid-template-columns: 30% 70%;
        grid-template-rows: auto auto auto auto auto;
    }

    /* .field-label {
        font-weight: normal;
        color: var(--primary);
        font-size: 20px;
    }

    #done-button {
        float: right;
    } */


    h1 {
        font-weight: 700;
        color: var(--accent);
        font-size: 30px;
    }
</style>
