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
    import MonthlyCalendarBase from '$lib/components/MonthlyCalendarBase.svelte'; 

    // strings
    import strings from "$lib/strings.json";
    import { exclude_internal_props } from 'svelte/internal';
    import { parseISO } from 'date-fns';

    // calendar visibilities and variables
    let name;
    let start, show_start_cal;
    let end, show_end_cal;
    let lockin, show_lockin_cal;
    let length;

    // this needs to be a ARRAY
    // user + priority
    let users=[["", 1]];

    // TODO handfisted input validaition
    function validate() {
        if (start == undefined) {
            alert(strings.MEETING_VALIDATE_MISSING_START);
            return false;
        } else if (end == undefined) {
            alert(strings.MEETING_VALIDATE_MISSING_END);
            return false;
        } else if (lockin == undefined) {
            alert(strings.MEETING_VALIDATE_MISSING_LOCKIN);
            return false;
        } else if (isNaN(parseInt(length))) {
            alert(strings.MEETING_VALIDATE_MISSING_LENGTH);
            return false;
        }
        return true;
    }


    // to replace button
    let bottomText=null;

    // quick utility function to check if
    // users are clicking the calendar
    function isClickCalendar(e) {
        return (e.relatedTarget &&
                e.relatedTarget.classList.contains("hover"));
    }

    // check if users are clicking on item of id
    function isClickID(e, id) {
        return (e.relatedTarget &&
                e.relatedTarget.id == id);
    }



    async function submitMeeting() {
        // validate
        if (validate() == false) return;

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
            // TODO (make persistent users when auth is done) make
            // a user and staple the ticket to the user
            let user_req = fetch(user_endpoint.href, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: "TODO",
                    email:email, // TODO, but trying to scehdule most for now
                })
            });
            let uid = ((await (await user_req).json()).id);
            // generate a meeting subscription ticket
            let sub_req = fetch(meeting_sub_endpoint.href, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    weight: weight,
                    user: uid,
                    meeting: meeting_id,
                    isCritical: false // TODO, but trying to scehdule most for now
                })
            });
            // send request and wait for it to finish
        }

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
                   id="start"
                   placeholder="{strings.MEETING_START_PLACEHOLDER}"
                   bind:value={start}
                   on:focus={()=>show_start_cal=true}
                   on:blur={(e)=>{
                       if (!isClickCalendar(e)) show_start_cal=false;
                   }}
                   on:change={()=>{
                       // parse the date
                       let parsed = chrono.parseDate(start, (new Date()), {forwardDate: true});
                       if (parsed) {
                        // format the date and set to string
                        start = format(parsed, strings.UNIVERSAL_DATE_FORMAT);
                       } else {start = undefined;}

                   }} required/>

            <div class="hover"
                 tabindex="0"
                 style:display="{show_start_cal?'inline':'none'}"
                 on:blur={(e)=>{
                    if (!isClickID(e, "start")) show_start_cal=false;
                 }}>
                <MonthlyCalendarBase
                    selection={!isNaN(Date.parse(start)) ?
                        (new Date(start)): null}
                    month={!isNaN(Date.parse(start)) ?
                        (new Date(start)).getMonth()+1: (new Date()).getMonth()+1}
                    year={!isNaN(Date.parse(start)) ?
                        (new Date(start)).getFullYear(): (new Date()).getFullYear()}
                    on:select={(e)=> {start = format(e.detail.date,
                    strings.UNIVERSAL_DATE_FORMAT); show_start_cal=false}} />
            </div>


            <h2 class="meeting-subhead">{strings.MEETING_END}</h2>
            <input type="text"
                   id="end"
                   placeholder="{strings.MEETING_END_PLACEHOLDER}"
                   on:focus={()=>show_end_cal=true}
                   on:blur={(e)=>{
                       if (!isClickCalendar(e)) show_end_cal=false;
                   }}
                   bind:value={end}
                   on:change={()=>{
                       // parse the date
                       let parsed = chrono.parseDate(end, (new Date()), {forwardDate: true});
                       if (parsed) {
                        // format the date and set to string
                        end = format(parsed, strings.UNIVERSAL_DATE_FORMAT);
                       } else {end = undefined;}
                   }} required/>

            <div class="hover"
                 tabindex="0"
                 style:display="{show_end_cal?'inline':'none'}"
                 on:blur={(e)=>{
                    if (!isClickID(e, "end")) show_end_cal=false;
                 }}>
                <MonthlyCalendarBase
                    selection={!isNaN(Date.parse(end)) ?
                        (new Date(end)): null}
                    month={!isNaN(Date.parse(end)) ?
                        (new Date(end)).getMonth()+1: (new Date()).getMonth()+1}
                    year={!isNaN(Date.parse(end)) ?
                        (new Date(end)).getFullYear(): (new Date()).getFullYear()}
                    on:select={(e)=> {end = format(e.detail.date,
                    strings.UNIVERSAL_DATE_FORMAT); show_end_cal=false}} />

            </div>

            <h2 class="meeting-subhead">{strings.MEETING_LOCKIN}</h2>
            <input type="text"
                   id="lockin"
                   on:focus={()=>show_lockin_cal=true}
                   on:blur={(e)=>{
                       if (!isClickCalendar(e)) show_lockin_cal=false;
                   }}
                   placeholder="{strings.MEETING_LOCKIN_PLACEHOLDER}"
                   bind:value={lockin}
                   on:change={()=>{
                       // parse the date
                       let parsed = chrono.parseDate(lockin, (new Date()), {forwardDate: true});
                       if (parsed) {
                        // format the date and set to string
                        lockin = format(parsed, strings.UNIVERSAL_DATE_FORMAT);
                       } else {lockin = undefined;}

                   }} required/>
            <div class="hover"
                 tabindex="0"
                 style:display="{show_lockin_cal?'inline':'none'}"
                 on:blur={(e)=>{
                    if (!isClickID(e, "lockin")) show_lockin_cal=false;
                 }}>
                <MonthlyCalendarBase
                    selection={!isNaN(Date.parse(lockin)) ?
                        (new Date(lockin)): null}
                    month={!isNaN(Date.parse(lockin)) ?
                        (new Date(lockin)).getMonth()+1: (new Date()).getMonth()+1}
                    year={!isNaN(Date.parse(lockin)) ?
                        (new Date(lockin)).getFullYear(): (new Date()).getFullYear()}
                    on:select={(e)=> {lockin = format(e.detail.date,
                    strings.UNIVERSAL_DATE_FORMAT); show_lockin_cal=false}} />
            </div>

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

    #create-form {
        padding: 20px;
    }

    .hover {
        position: fixed;
        left: 0;
        background: var(--accented-background);
        z-index: 5;
        padding: 0 6px 10px 14px;
        display: inline;
        transform: scale(0.7) translateX(70vw) translateY(-25px);
        border-radius: 10px;
        border: 1px solid var(--tertiary);
    }

</style>
