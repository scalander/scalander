<svelte:head>
    <script src="https://accounts.google.com/gsi/client" on:load={loadGoogle} />
</svelte:head>


    <script>
    // page info and svelte tooling
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    // our own UI components
    import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"
    import Button from '$lib/components/ui/Button.svelte';

    // our calendar helper
    import { freebusyHelper } from "$lib/components/calengine.js";

    // strings
    import strings from "$lib/strings.json";
import { exclude_internal_props, validate_component } from 'svelte/internal';

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
    let oauth_ready = false;

    // the freebusy info we are fetching
    let freebusy_loading = false;

    // our datepicker component
    let datepicker_component;

    // handle credential input
    async function handleCredential(authResult) {
        // create the call URL (passing in our endpoint URL
        let endpoint = new URL("api/freebusy",
                               import.meta.env.VITE_BACKEND_ENDPOINT);
        let req = fetch(endpoint.href, {
            method: "GET",
            headers: {"Authorization": `Bearer ${authResult.access_token}`}
        });

        // let the user know that we are loading
        freebusy_loading = true;

        // load freebusy
        let res = await (await req).json();

        // calculate gaps and set to calendars
        change = freebusyHelper(res);
        datepicker_component.set(change);

        // move on
        freebusy_loading = false;
        state = 2;
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
                scope: "https://www.googleapis.com/auth/calendar.readonly"
            });
            oauth_ready = true;
        } catch (e) {
            console.log("google is not ready yet, will retry.");
            // TODO WARN
            // this is usually when the API is not ready yet
        }
    };
</script>


<div id="page-container">
    <div id="schedule-container"
         class="schedule-container-{state!=2?'small':'large'}">
        <!-- we use DISPLAY instead of IF here because we want to -->
        <!-- keep the calendar, etc., mounted -->
        <div style:display="{state==1?'block':'none'}">
            <h1>{strings.SCHEDULE_FIND_TIME}</h1>
            <p>{strings.SCHEDULE_DESCRIPTION}</p>
            <div class="schedule-action-container">
                <div id="schedule-action-buttons">
                    {#if freebusy_loading}
                        Loading your Calendars...
                    {:else}
                        {#if oauth_ready}
                        <Button primary
                                on:click={()=>client.requestAccessToken()}>
                            {strings.SCHEDULE_READ_CAL}</Button>
                        or
                        {/if}
                        <Button primary
                                on:click={()=>state=2}>
                            {strings.SCHEDULE_PICK_MANUALLY}</Button>
                    {/if}
                </div>
            </div>
        </div>
        <div style:display="{state==2?'block':'none'}">
            <div>
                <span class="action"
                        on:click={()=>state=1}>
                    <i class="fa-solid fa-chevron-left action" />
                    {strings.GLOBAL_BACK}
                </span>
                <span class="action right"
                        on:click={submitResult}><i class="fa-solid fa-check action"></i> {strings.GLOBAL_DONE}</span>
            </div>
            <DateTimeRangePicker
                bind:this={datepicker_component}
                on:change="{(e)=> change=e.detail.selected}"/>
        </div>
        <div class="schedule-center-container" style:display="{state==3?'block':'none'}">
            <div>
                <h1>🎉 {strings.SCHEDULE_CONGRATS}</h1>
                <p style="font-weight: 500; padding-top: 10px">{strings.SCHEDULE_CONGRATS_MSG}</p>
            </div>
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
