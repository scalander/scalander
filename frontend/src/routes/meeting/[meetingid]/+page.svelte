<script>
    // page info and svelte tooling
    import { page } from '$app/stores';

    // date fns
    import { format, formatDistance } from "date-fns";

    // onload
    import { onMount } from "svelte";

    // strings
    import strings from "$lib/strings.json";

    let meeting_promise = new Promise(()=>{}); 

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

        // again, the best proposal is the one on the top
        // we also slice it out
        let best_proposal = proposals.slice(0, 1)[0];
        // we index by 0 because the sliced result is a list

        // set proposals
        meeting_info["proposals"] = proposals;
        return [meeting_info, best_proposal];
    }

    onMount(()=>{
        meeting_promise=meetingLoad();
    });
</script>

<div class="centering-container">
    <span class="centered">
        {#await meeting_promise}
            Loading...
        <!-- new meeting object doesn't include the best proposal -->
        <!-- as we hope to access it directly -->
    {:then [meeting, bestProposal]} 
        <h1 id="meeting-name">{meeting.name}</h1>
        <span id="meeting-length">{formatDistance(0, meeting.length*60*1000)}</span>
        <br />
        <span class="date">{format((new Date(bestProposal.start)), "EEEE, MMMM dd yyyy")}</span>
        <div class="time">
            <span class="start-time">{format((new Date(bestProposal.start)), "hh:mm aa")}</span> — <span class="end-time">{format((new Date(bestProposal.end)), "hh:mm aa")}</span>
        </div>
        <span class="sublabel">{strings.RESULT_AVAILABLE}</span>
        {#each bestProposal.commitedUsers as commited}
            <span class="email">{commited.emails}</span>
            <!-- TODO plural because user email is plural (aaa) -->
        {/each}
        <span class="sublabel">{strings.RESULT_UNAVAILABLE}</span>
        {#each bestProposal.unavailableUsers as commited}
            <span class="email">{commited.emails}</span>
            <!-- TODO plural because user email is plural (aaa) -->
        {/each}

        {/await}
    </span>
</div>

<style>
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
        font-size: 12px;
        margin-top: 15px;
        display: inline-block;
    }

    .email {
        display: block;
    }
</style>
