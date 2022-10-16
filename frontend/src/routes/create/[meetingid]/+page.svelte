<svelte:head>
    <script src="https://accounts.google.com/gsi/client" on:load={loadGoogle} />
</svelte:head>

<!-- base copied from ./schedule/[uid] -->

<script>
    // page info and svelte tooling
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    // our own UI components
    import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"
    import Button from '$lib/components/ui/Button.svelte';

    // strings
    import strings from "$lib/strings.json";
    import { exclude_internal_props } from 'svelte/internal';

    // current changes
    let change = []

    // the button
    let gbutton;

    // global state
    // state 1 is "google or manual" screen
    // state 2 is the datepicker + submit screen
    // state 3 is the completion screen
    let state = 1;
    // wheather google is ready
    let ready = false;

    // handle credential input
    function handleCredential(authResult) {
        // TODO pass it to the server
        console.log(`amazing physics going on with ${authResult.access_token}`);
        // move on
        state=2
    }

    // submit result
    function submitResult() {
        // TODO pass it to hte server
        console.log(`amazing physics going on with ${change}`);
        // move on
        state=3
    }

    onMount(loadGoogle);

    let client;

    // Initialize Google Credential Services
    function loadGoogle() {
        try {
            client = google.accounts.oauth2.initTokenClient({
                client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
                callback: handleCredential,
                scope: "https://www.googleapis.com/auth/calendar.readonly "
            });
            ready = true;
        } catch (e) {
            console.log(e);
            // TODO WARN
            // this is usually when the API is not ready yet
        }
    };
</script>


<div id="page-container">
    <div id="schedule-container"
         class="schedule-container-{state!=2?'small':'large'}">
        <!-- State 1 is a "what do you want to do" screen -->
        {#if state==1}
            <h1>{strings.SCHEDULE_FIND_TIME}</h1>
            <p>{strings.SCHEDULE_DESCRIPTION}</p>
            <div class="schedule-action-container">
                <div id="schedule-action-buttons">
                    {#if ready}
                    <Button primary
                            on:click={()=>client.requestAccessToken()}>
                        {strings.SCHEDULE_READ_CAL}</Button>
                    or
                    {/if}
                    <Button primary
                            on:click={()=>state=2}>
                        {strings.SCHEDULE_PICK_MANUALLY}</Button>
                </div>
            </div>
        {:else if state == 2}
            <div>
                <div>
                    <span class="action"
                           on:click={()=>state=1}>
                        <i class="fa-solid fa-chevron-left action" />
                        {strings.GLOBAL_BACK}
                    </span>
                    <span class="action right"
                          on:click={submitResult}><i class="fa-solid fa-check action"></i> {strings.GLOBAL_DONE}</span>
                </div>
                <DateTimeRangePicker on:change="{(e)=> change=e.detail.selected}"/>
            </div>
        {:else}
            <div class="schedule-center-container">
                <div>
                    <h1>🎉 {strings.SCHEDULE_CONGRATS}</h1>
                    <p style="font-weight: 500; padding-top: 10px">{strings.SCHEDULE_CONGRATS_MSG}</p>
                </div>
            </div>
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

    #schedule-container {
        background: var(--accented-background);
        border-radius: 5px;
        padding: 20px;
    }
    .schedule-container-small {
        width: min(80vw, 500px);
        height: min(80vh, 250px);
    }
    .schedule-container-large {
        width: min(80vw, 700px);
        height: min(80vh, 450px);
    }

    .schedule-action-container {
        height: calc(min(80vh, 250px) - 150px);
        justify-content: center;
        align-items: center;
        display: flex;
    }

    .schedule-center-container {
        width: 100%;
        height: 100%;
        justify-content: center;
        align-items: center;
        display: flex;
    }

    #schedule-action-buttons {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 30px;
        color: var(--accent);
    }

    #done-button {
        float: right;
    }

    .action {
        color: var(--accent);
        cursor: pointer;
    }

    .right {
        float: right;
    }

    h1 {
        font-weight: 700;
        color: var(--accent);
        font-size: 30px;
    }
</style>
