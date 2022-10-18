<script>
    //chrono
    import * as chrono from 'chrono-node';
    import { format } from 'date-fns'
    //do format("yyyy-MM-dd HH:mm:ss")
    //

    // page info and svelte tooling
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    // our own UI components
    // import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"
    import Button from '$lib/components/ui/Button.svelte';

    // strings
    import strings from "$lib/strings.json";
    import { exclude_internal_props } from 'svelte/internal';
    import { parseISO } from 'date-fns';

    let name;
    let start;
    let end;
    // this needs to be a ARRAY
    // user + priority
    let users=[["", 1]];

    </script>


<div id="page-container">
    <div id="create-form">
        <h1>{strings.CREATE_A_MEETING}</h1>
        <form class = "meeting-form"> <!-- TODO: make a thing for input fields bc listing all of them here is hella messy -->
            <h2 class="meeting-subhead">{strings.MEETING_NAME}</h2>
            <input type="text"
                   placeholder="{strings.MEETING_NAME_PLACEHOLDER}"
                   bind:value={name} />

            <h2 class="meeting-subhead">{strings.MEETING_START}</h2>
            <input type="text"
                   placeholder="{strings.MEETING_START_PLACEHOLDER}"
                   bind:value={start}
                   on:change={()=>{
                       // parse the date
                       let parsed = chrono.parseDate(start, {forwardDate: true});
                       // format the date and set to string
                       // TODO internationalize the freedom units
                       start = format(parsed, "EEEE, MMMM dd yyyy");
                   }}/>

            <h2 class="meeting-subhead">{strings.MEETING_END}</h2>
            <input type="text"
                   placeholder="{strings.MEETING_END_PLACEHOLDER}"
                   bind:value={end}
                   on:change={()=>{
                       // parse the date
                       let parsed = chrono.parseDate(end, {forwardDate: true});
                       // format the date and set to string
                       // TODO internationalize the freedom units
                       end = format(parsed, "EEEE, MMMM dd yyyy");
                   }}/>
            <hr />
            <h2 class="meeting-subhead"
                style:margin="10px 0 0 0">{strings.MEETING_INVITEES}</h2>
            <span id="priority-explanation">{strings.MEETING_PRIORITY}</span>
            {#each users as user, i} 
                <div class="userbox">
                    <input type="email"
                           class="userleft"
                           placeholder="{strings.MEETING_EMAIL_PLACEHOLDER}"
                           bind:value={user[0]}/>
                    <input type="email"
                           class="userright"
                           placeholder="1"
                           bind:value={user[1]}/>
                    <div class="usericon">
                        {#if i!=0}
                        <i class="fa-solid fa-trash icon"
                           on:click="{()=>{users.splice(i, 1);
                                           // reset to trigger render
                                           users=users;}}"></i>
                        {/if}
                        {#if i==(users.length-1)}
                            <i class="fa-solid fa-plus icon"
                               on:click="{()=>{users.push(["", 1]);
                                               // reset to trigger render
                                               users=users;}}"></i>
                        {/if}
                    </div>
                </div>
            {/each} 
        </form>
        <div id="submit">
            <Button primary>{strings.MEETING_SUBMIT}</Button>
        </div>
    </div>
</div>


<style>
    .userbox {
        display: flex;
    }

    .userleft {
        width: inherit;
        flex-grow: 1;
        max-width: 500px;
        width: min(500px, 70vw);
    }

    .userright {
        width: inherit;
        flex-shrink: 1;
        width: 50px;
        text-align: center !important;
        margin: 5px 10px;
    }

    #page-container{
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    h1 {
        font-weight: 700;
        color: var(--accent);
        font-size: 30px;
    }

    .meeting-subhead {
        color: var(--secondary);
        font-size: 13px;
        font-weight: 600;
    }

    #priority-explanation {
        color: var(--secondary);
        font-size: 12px;
        transform: translateY(-2px);
        display: block;
    }


    input {
        margin-bottom: 15px;
        font-size: 15px;
        padding: 5px;
        margin: 5px 0;
        max-width: 600px;
        width: min(90vw, 600px);
        border: 1px solid transparent;
        border-radius: 5px;
        transition: border-color 0.2s linear;
    }

    input:hover {
        border: 1px solid var(--tertiary);
    }

    input:focus {
        border: 1px solid var(--accent);
        outline: 0;
    }

    #submit {
        margin-top: 20px;
    }

    .usericon {
        display: flex;
        align-items: center;
        gap: 13px;
        font-size: 13px;
    }

    .icon {
        color: var(--accent);
        cursor: pointer;
        opacity: 0.9;
        transition: opacity 0.3s linear;
    }

    .icon:hover {
        opacity: 1;
    }

</style>
