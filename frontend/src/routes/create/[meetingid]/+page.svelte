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
    let start //use DateTimeRangePicker for start end?
    let end
    let users //stores emails separated by commas
    let lockIn
    let meeting = {}

    function submit(name, start, end, users, lockIn){ //name = string, start = string, end = string, users = [User], lockIn = string
        let meetingInfo = (name,start,end,users,lockIn)
        console.log(meetingInfo)
    }

</script>


<div id="page-container">
    {#if state==1}
        <!-- State 1 is the form -->
        <div id="meeting-form">
            <h1>{strings.CREATE_A_MEETING}</h1>
            <form class = "meeting-form"> <!-- TODO: make a thing for input fields bc listing all of them here is hella messy -->
                <h2>{strings.MEETING_NAME}</h2>
                <input type = "text" bind:value={name} />

                <h2>{strings.MEETING_START}</h2>
                <input type = "text" bind:value={start} />

                <h2>{strings.MEETING_END}</h2>
                <input type = "text" bind:value={end} />

                <h2>{strings.MEETING_USERS}</h2>
                <input type = "text" bind:value={users} />
                
                <h2>{strings.MEETING_LOCK_IN}</h2>
                <input type = "text" bind:value={lockIn} />
            </form>
            <Button primary
                            on:click={()=>submit({name},{start},{end},{users},{lockIn})}>
                        {strings.SUBMIT}</Button>
        </div>
    {/if}
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
        display: flex;
        gap: 100px 200px;
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

    h2 {
        font-weight: normal;
        color: var(--primary);
        font-size: 20px;
    }
</style>
