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

        async function fetch_proposal(proposal) {
            // meeting info endpoint
            endpoint = new URL(`api/proposal/${proposal}`,
                               import.meta.env.VITE_BACKEND_ENDPOINT);
            req = fetch(endpoint.href);
            // get proposal info
            let proposal_json = await ((await req).json());
            return proposal_json;
        }

        let proposals = await Promise.all(proposal_ids.map(fetch_proposal));

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
        <span class="date">{format((new Date(meeting.proposals[view_proposal].start)), strings.UNIVERSAL_DATE_FORMAT)}</span>
        <div class="time">
            <span class="start-time">{format((new Date(meeting.proposals[view_proposal].start)), strings.UNIVERSAL_TIME_FORMAT)}</span> — <span class="end-time">{format((new Date(meeting.proposals[view_proposal].end)), strings.UNIVERSAL_TIME_FORMAT)}</span>
        </div>
        <div class="availability" style="margin-bottom: 20px">
            <div>
                <span class="sublabel">{strings.RESULT_AVAILABLE} ({meeting.proposals[view_proposal].commitedUsers.length})</span>
                {#each meeting.proposals[view_proposal].commitedUsers as commited}
                    <span class="email">{commited.email}</span>
                {/each}
            </div>
            <div>
                <span class="sublabel">{strings.RESULT_UNAVAILABLE} ({meeting.proposals[view_proposal].unavailableUsers.length})</span>
                {#each meeting.proposals[view_proposal].unavailableUsers as uncommited}
                    <span class="email">{uncommited.email}</span>
                {/each}
            </div>
        </div>

        <!-- If we are not locked in yet -->
        {#if (new Date())<(new Date(meeting.lock_in_date))}
        <hr />
        <span class="sublabel">{strings.RESULT_ALTERNATE}</span> <span class="order">{strings.RESULT_ORDERING}</span>
        <div class="buttonrow">
        {#each [...Array(number_plans).keys()] as t}
            <div class={"button "+((t==view_proposal)?"active":"")}
                 on:click={()=>{view_proposal=t}}>{t+1}</div>
        {/each}
        </div>
        <span id="lockin">{strings.MEETING_LOCK_IN.replace("{date}", format(new Date(meeting.lock_in_date), strings.UNIVERSAL_DATE_FORMAT))}</span>
        {/if}
        {:else}
            <div id="notscheduled">
            <div id="notscheduled-msg">{strings.MEETING_NOT_SCHEDULED}</div>
            <span class="sublabel">{strings.MEETING_RANGE}</span> 
            <p class="bold">{format((new Date(meeting.start)), strings.UNIVERSAL_DATE_FORMAT)} — {format((new Date(meeting.end)), strings.UNIVERSAL_DATE_FORMAT)}</p>
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
        margin-top: 2px;
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

    #lockin {
        display: block;
        font-size: 11px;
        transform: translateX(-1px);
        color: var(--accent);
    }
</style>
