<script>
    export let data;
</script>

<h1>{data.meeting.name}</h1>

Starts at {(new Date(data.meeting.start)).toLocaleString()}
Ends at {(new Date(data.meeting.end)).toLocaleString()}
Added users:
<ul>
    {#each data.meeting.subscribedUsers as attendee}
        <li>{JSON.stringify(attendee)}</li>
    {/each}
</ul>
Proposed times:
<ul>
    {#each data.meeting.proposals as proposal}
        <li>{JSON.stringify(proposal)}</li>
    {/each}
</ul>