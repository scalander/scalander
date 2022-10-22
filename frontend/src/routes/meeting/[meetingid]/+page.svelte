<script>
    // page info and svelte tooling
    import { page } from '$app/stores';

    // date fns
    import { format, formatDistance } from "date-fns";

    // onload
    import { onMount } from "svelte";

    // strings
    import strings from "$lib/strings.json";

    // our own UI components
    import Button from '$lib/components/ui/Button.svelte';

    let meeting_promise = new Promise(()=>{}); 

    // get number of plans
    let number_plans = 0;
    // view the nth number of proposals
    let view_proposal = 0;

    async function meetingLoad() {
        // recyclable variables
        let endpoint, req;
        // meeting info endpoint
        endpoint = new URL(`api/meeting/${$page.params.meetingid}`,
                           import.meta.env.VITE_BACKEND_ENDPOINT);
        req = fetch(endpoint.href);
        // get meeting info
        let meeting_info = await ((await req).json());

        // we now parse meeting info, getting a few things along the way
        // recall that .start and .end are the possible START RANGES
        // so, to get the actual "official" start time, we pick the one
        // that's on the top of the list of proposals. However, to
        // display the other times, we also will get all the proposas.

        let proposal_ids = meeting_info.proposals;
        let proposals = [];

        for (let proposal of proposal_ids) {
            // meeting info endpoint
            endpoint = new URL(`api/proposal/${proposal}`,
                               import.meta.env.VITE_BACKEND_ENDPOINT);
            req = fetch(endpoint.href);
            // get proposal info
            let proposal_json = await ((await req).json());
            proposals.push(proposal_json);
        }

        // get proposal number
        number_plans = proposals.length;

        // set proposals
        meeting_info["proposals"] = proposals;
        return meeting_info;
    }

    onMount(()=>{
        meeting_promise=meetingLoad();
    });
</script>

<div class="centering-container">
    <span class="centered">
        {#await meeting_promise}
            <span class="loading">Loading...</span>
        <!-- new meeting object doesn't include the best proposal -->
        <!-- as we hope to access it directly -->
        {:then meeting} 
        <h1 id="meeting-name">{meeting.name}</h1>
        <span id="meeting-length">{formatDistance(0, meeting.length*60*1000)}</span>
        {#if meeting.proposals.length > 0}
        <br />
        <span class="date">{format((new Date(meeting.proposals[view_proposal].start)), "EEEE, MMMM dd yyyy")}</span>
        <div class="time">
            <span class="start-time">{format((new Date(meeting.proposals[view_proposal].start)), "hh:mm aa")}</span> — <span class="end-time">{format((new Date(meeting.proposals[view_proposal].end)), "hh:mm aa")}</span>
        </div>
        <div class="availability" style="margin-bottom: 20px">
            <div>
                <span class="sublabel">{strings.RESULT_AVAILABLE} ({meeting.proposals[view_proposal].commitedUsers.length})</span>
                {#each meeting.proposals[view_proposal].commitedUsers as commited}
                    <span class="email">{commited.emails}</span>
                    <!-- TODO plural because user email is plural (aaa) -->
                {/each}
            </div>
            <div>
                <span class="sublabel">{strings.RESULT_UNAVAILABLE} ({meeting.proposals[view_proposal].unavailableUsers.length})</span>
                {#each meeting.proposals[view_proposal].unavailableUsers as uncommited}
                    <span class="email">{uncommited.emails}</span>
                    <!-- TODO plural because user email is plural (aaa) -->
                {/each}
            </div>
        </div>

        <hr />

        <span class="sublabel">{strings.RESULT_ALTERNATE}</span> <span class="order">{strings.RESULT_ORDERING}</span>
        <div class="buttonrow">
        {#each [...Array(number_plans).keys()] as t}
            <div class={"button "+((t==view_proposal)?"active":"")}
                 on:click={()=>{view_proposal=t}}>{t+1}</div>
        {/each}
        </div>
        {:else}
            <div id="notscheduled">
            <div id="notscheduled-msg">{strings.MEETING_NOT_SCHEDULED}</div>
            <span class="sublabel">{strings.MEETING_RANGE}</span> 
            <p class="bold">{format((new Date(meeting.start)), "EEEE, MMMM dd yyyy")} — {format((new Date(meeting.end)), "EEEE, MMMM dd yyyy")}</p>
            </div>
        {/if}


        {/await}
</div>

<style>

    .button {
        background-color: var(--tertiary);
        color: var(--accent);
        display: flex;
        justify-content: center;
        align-items: center;
        flex-grow: 1;
        cursor: pointer;
        transition: opacity 0.2s linear;
    }

    .active {
        color: var(--tertiary) !important;
        background-color: var(--accent) !important;
    }

    .button:hover {
        opacity: 0.8;
    }

    .buttonrow {
        display: flex;
        width: 100%;
    }

    .centering-container {
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #meeting-name {
        color: var(--accent);
        font-weight: 700;
        font-size: 30px;
        display: inline;
    }

    #meeting-length {
        font-size: 11px;
        color: var(--accent);
        font-weight: 300;
        display: inline-block;
    }

    .date {
        font-weight: 600;
    }

    .sublabel {
        color: var(--accent);
        font-weight: 700;
        font-size: 13px;
        margin-top: 15px;
        display: inline-block;
    }

    .email {
        display: block;
        font-size: 14px;
        font-weight: 300;
    }

    .availability {
        display: flex;
        gap: 60px;
        flex-wrap: wrap;
    }

    .loading {
        color: var(--accent);
        font-weight: 600;
    }

    .order {
        color: var(--accent);
        font-size: 10px;
        float:right;
        transform: translateY(18px);
    }

    #notscheduled {
        max-width: min(500px, 90vw)
    }

    #notscheduled-msg {
        font-weight: 300;
    }

    .bold {
        font-weight: 600;
    }
</style>
