<svelte:head>
    <script src="https://accounts.google.com/gsi/client" />
</svelte:head>


    <script>
    // page info and svelte tooling
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    // our own UI components
    import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"
    import Button from '$lib/components/ui/Button.svelte';

    // strings
    import strings from "$lib/strings.json";

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
        console.log(`amazing physics going on with ${authResult.credential}`);
        // move on
        state=2
    }

    // Initialize Google Credential Services
    onMount(()=>{
        google.accounts.id.initialize({
            client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
            callback: handleCredential,
            native_callback: handleCredential,
            auto_select: true
        });
        ready = true;
    });

    $: {
        // if ready and right state, render button
        if (ready && state == 1) {
            google.accounts.id.renderButton(
                gbutton,
                { theme: "outline",
                  size: "large",
                  width: 100 } 
            );
        }
    }

</script>


<div id="page-container">
    <div id="schedule-container"
         class="schedule-container-{state==1?'small':'large'}">
        <!-- State 1 is a "what do you want to do" screen -->
        {#if state==1}
            <h1>{strings.SCHEDULE_FIND_TIME}</h1>
            <p>{strings.SCHEDULE_DESCRIPTION}</p>
            <div id="schedule-action-container">
                <div id="schedule-action-buttons">
                    <span bind:this={gbutton} id="gbutton"></span>
                    or
                    <Button primary
                            on:click={()=>state=2}>
                        {strings.SCHEDULE_PICK_MANUALLY}</Button>
                </div>
            </div>
        {:else}
            <div>
                <div>
                    <span class="action"
                           on:click={()=>state=1}>
                        <i class="fa-solid fa-chevron-left action" />
                        {strings.GLOBAL_BACK}
                    </span>
                    <span class="action right"><i class="fa-solid fa-check action"></i> {strings.GLOBAL_DONE}</span>
                </div>
                <DateTimeRangePicker on:change="{(e)=> change=e.detail.selected}"/>
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

    #schedule-action-container {
        height: calc(min(80vh, 250px) - 150px);
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
