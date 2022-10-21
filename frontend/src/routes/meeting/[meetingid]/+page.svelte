<script>
    // page info and svelte tooling
    import { page } from '$app/stores';

    let meeting_promise = (async function() {
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
        console.log(proposals);

        // again, the best proposal is the one on the top
        // we also slice it out
        let best_proposal = proposals.slice(0, 1);

        return meeting_info;
    })();
</script>

{#await meeting_promise}

    te
{:then meeting}
    <h1>{meeting.name}</h1>

    Starts at {(new Date(meeting.start)).toLocaleString()}
    Ends at {(new Date(meeting.end)).toLocaleString()}
    Added users:
    <ul>
        {#each meeting.subscribedUsers as attendee}
            <li>{JSON.stringify(attendee)}</li>
        {/each}
    </ul>
    Proposed times:
    <ul>
        {#each meeting.proposals as proposal}
            <li>{JSON.stringify(proposal)}</li>
        {/each}
    </ul>
{/await}
