<script>
    //chrono
    import * as chrono from 'chrono-node';
    import { format, subDays } from 'date-fns'
    //do format("yyyy-MM-dd HH:mm:ss")
    //

    // page info and svelte tooling
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    // our own UI components
    import Button from '$lib/components/ui/Button.svelte';

    // strings
    import strings from "$lib/strings.json";
    import { exclude_internal_props } from 'svelte/internal';
    import { parseISO } from 'date-fns';

    let name;
    let start;
    let end;
    let length;
    let lockin;
    // this needs to be a ARRAY
    // user + priority
    let users=[["", 1]];

    // to replace button
    let bottomText=null;

    async function submitMeeting() {
        // set bottom text
        bottomText = strings.MEETING_LOADING;


        // TODO this function is too large
        // it....
        // 1. creates a meeting object
        // 2. create user subscription objects for each user
        // 3. creates the user behind it
        // create the call URL (passing in our endpoint URL
        let meeting_endpoint = new URL("api/meeting",
                               import.meta.env.VITE_BACKEND_ENDPOINT);
        let meeting_req = fetch(meeting_endpoint.href, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name,
                start: new Date(start),
                end: new Date(end),
                length,
                lockInDate: new Date(lockin), // TODO we hard-code meetings to be scheduled by this time; we can also just ask the user
                proposals: [],
                subscribedUsers: [],
            })
        });

        // get the newly created meeting ID
        let meeting_id = (await (await meeting_req).json()).id;

        // create a tally of meeting subscription tickes
        let sub_tickets = [];

        // for each user, we work on their data
        let meeting_sub_endpoint = new URL("api/attendance",
                                            import.meta.env.VITE_BACKEND_ENDPOINT);
        let user_endpoint = new URL("api/user",
                                     import.meta.env.VITE_BACKEND_ENDPOINT);
        for (let [email,weight] of users) {
            // generate a meeting subscription ticket
            let sub_req = fetch(meeting_sub_endpoint.href, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    weight: weight,
                    meeting: meeting_id,
                    isCritical: false // TODO, but trying to scehdule most for now
                })
            });
            let sub_id = ((await (await sub_req).json()).id);
            // TODO (make persistent users when auth is done) make
            // a user and stamp the ticket to the user
            let user_req = fetch(user_endpoint.href, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: "TODO",
                    emails:email, // TODO, but trying to scehdule most for now
                    //// AAAAAA email is plural
                    commitments: [], // backend will send email for form
                    meetingSubscriptions: [sub_id] // stamping with our ticket
                })
            });
            // send request and wait for it to finish
            await user_req;
            sub_tickets.push(sub_id);
        }

        let meeting_new_endpoint = new URL(`api/meeting/${meeting_id}`,
                               import.meta.env.VITE_BACKEND_ENDPOINT);
        let meeting_update_req = fetch(meeting_new_endpoint.href, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // TODO we need to supply all the meeting info again
                // because PUT overwrites
                name,
                start: new Date(start),
                end: new Date(end),
                length,
                lockInDate: new Date(lockin), // TODO we hard-code meetings to be scheduled by this time; we can also just ask the user
                proposals: [],
                subscribedUsers: sub_tickets,
            })
        });

        await meeting_update_req;
        bottomText = strings.MEETING_DONE;


    }

    </script>


<div id="page-container">
    <div id="create-form">
        <h1>{strings.CREATE_A_MEETING}</h1>
        <form class = "meeting-form"> <!-- TODO: make a thing for input fields bc listing all of them here is hella messy -->
            <h2 class="meeting-subhead">{strings.MEETING_NAME}</h2>
            <input type="text"
                   placeholder="{strings.MEETING_NAME_PLACEHOLDER}"
                   bind:value={name} required />

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
                   }} required/>

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
                   }} required/>

            <h2 class="meeting-subhead">{strings.MEETING_LOCKIN}</h2>
            <input type="text"
                   placeholder="{strings.MEETING_LOCKIN_PLACEHOLDER}"
                   bind:value={lockin}
                   on:change={()=>{
                       // parse the date
                       let parsed = chrono.parseDate(lockin, {forwardDate: true});
                       // format the date and set to string
                       // TODO internationalize the freedom units
                       lockin = format(parsed, "EEEE, MMMM dd yyyy");
                   }} required/>

            <h2 class="meeting-subhead">{strings.MEETING_LENGTH}</h2>
            <input type="number"
                   placeholder="15"
                   bind:value={length} required/>
            <br />
            <br />
            <hr />
            <h2 class="meeting-subhead"
                style:margin="10px 0 0 0">{strings.MEETING_INVITEES}</h2>
            <span id="priority-explanation">{strings.MEETING_PRIORITY}</span>
            {#each users as user, i} 
                <div class="userbox">
                    <input type="email"
                           class="userleft"
                           placeholder="{strings.MEETING_EMAIL_PLACEHOLDER}"
                           bind:value={user[0]} required/>
                    <input type="email"
                           class="userright"
                           placeholder="1"
                           bind:value={user[1]} required/>
                    <div class="usericon">
                        {#if i!=0}
                            <a on:click="{()=>{users.splice(i, 1);
                                          // reset to trigger render
                                          users=users;}}">
                                <i class="fa-solid fa-trash icon"></i></a>
                            {/if}
                            {#if i==(users.length-1)}
                                <a on:click="{()=>{users.push(["", 1]);
                                                   // reset to trigger render
                                                   users=users;}}">
                                <i class="fa-solid fa-plus icon"></i></a>
                            {/if}
                            </div>
                </div>
            {/each} 
        </form>
        <div id="submit">
            {#if bottomText}
                <span id="bottomtext">{bottomText}</span>
            {:else}
                <Button primary
                        on:click={submitMeeting}>{strings.MEETING_SUBMIT}</Button>
            {/if}
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

    #bottomtext {
        color: var(--accent);
        font-size: 14px;
        font-weight: 600;
    }

</style>
