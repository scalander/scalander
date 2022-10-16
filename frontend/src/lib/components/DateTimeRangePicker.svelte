<script>
    // calendar
    import MonthlyCalendarBase from "./MonthlyCalendarBase.svelte";
    import Button from "./ui/Button.svelte";

    // event dispatching
    import { createEventDispatcher } from 'svelte';

    // crono
    import * as chrono from 'chrono-node';

    // date formatting
    import { format } from 'date-fns'

    // dispatcher
    const dispatch = createEventDispatcher();

    // currently selected times
    let selected = {
    };

    // function to set selections
    export function set(initial) {
        // create a temp stash to prevent state updates
        let tmpsel = {};

        // we will serialize selected to be the
        // initial list, responsivly
        for (const [start,end] of initial) {
            // get the date of initial availablitiy
            let date = new Date(start.getFullYear(),
                                start.getMonth(),
                                start.getDate());

            // TODO this REALLY shoulden't go here
            // but we will put it here anyways
            // if the END date is no longer the
            // START date (we moved days), we ignore
            // the date
            let endDate = new Date(end.getFullYear(),
                                   end.getMonth(),
                                   end.getDate());

            // note also that == compares date objects
            // and so .getTime() actually compares the dates
            if (date.getTime() != endDate.getTime()) {
                // skip; this is cross-days
                continue
            }

            // try to get the existing list
            let curr = tmpsel[date];
            // if doesn't exist, make it
            if (curr == undefined) {
                curr = [];
            } 
            // append to the list
            curr.push([start,end]);
            // set to the state
            // removing duplicates
            // TODO this is to fix a race condition
            // where svelte's async hydrate will update
            // state BEFORE props are updated
            tmpsel[date] = curr;
        }

        // set to the actual list, trigger state update
        selected = tmpsel;
    }
    
    // currently selected date
    let currentDate = null;

    // strings
    import strings from "$lib/strings.json";

    // function to dispatch change (with results)
    function dispatchChange() {
        let results = [];
        
        for (let key in selected) {
            results = [...results, ...(selected[key])];
        }

        dispatch('change', {selected:results});
    }

    // function to remove a selection
    function removeSelection(date, oldSelectionIndex) {
        let currentSelections = selected[date];
        // filter for current selection
        currentSelections.splice(oldSelectionIndex, 1);
        // if there is no length, we get rid of the key
        // otherwise, we set the new thing
        if (currentSelections.length == 0) {
            delete selected[date];
            // trigger svelte rerender
            selected = selected;
        } else {
            selected[date] = currentSelections;
        }

        // dispatch change
        dispatchChange();
    }

    // function to insert a selection
    function insertSelection(date, newSelection) {
        // check that the date conforms
        // otherwise, we need to update

        // get selections
        let currentSelections = selected[date] ? selected[date] : [];
        // append
        currentSelections.push(newSelection);
        // put it back
        selected[date] = currentSelections;

        // dispatch change
        dispatchChange();
    }

    // function to update a selection
    function updateSelection(date, oldSelectionIndex, newSelection) {
        let currentSelections = selected[date];
        // filter for current selection
        currentSelections.splice(oldSelectionIndex, 1, newSelection);
        // put it back
        selected[date] = currentSelections;

        // dispatch change
        dispatchChange();
    }

    // function to parse and update time
    function parseByTime(refDate, timeStr) {
        // TODO HACKY!!!
        // we add an "m" after stripping and if the last
        // character is `a` or p, because some
        // people like to write "5p" for "5pm", and
        // chrono doesn't parse that
        let timeStrClean = timeStr.trim()+(['a', 'p'].includes(timeStr[timeStr.length-1]) ?
                                           'm': '');
        // run chrono
        let date = chrono.parseDate(timeStrClean);
        // if the date doesn't parse, return to ref date
        if (!date) date=refDate;
        // set date
        date.setFullYear(refDate.getFullYear());
        date.setMonth(refDate.getMonth());
        date.setDate(refDate.getDate());
        // return
        return date
    }
</script>

<div class="wrapper">
    <MonthlyCalendarBase
        on:select={(e)=> currentDate = e.detail.date}
        mark={Object.keys(selected)} />

        <div class="selecter">
            {#if currentDate}
                <div class="date-subtitle">
                    {strings.DATETIMERANGEPICKER_SELECTING_TIME.replace("$DATE",
                    format(currentDate, "EEEE, MMMM dd, yyyy"))}
                </div>
                <div class="button-container">
                    {#if selected[currentDate]}
                        {#each selected[currentDate] as selection, i}
                            <div class="selection">
                                <span class="selection-content">
                                    <input class="datebox"
                                           value="{format(selection[0], 'hh:mm aa')}"
                                           on:change="{(e)=>updateSelection(currentDate,
                                                      i,
                                                      [parseByTime(currentDate, e.target.value),
                                                      selection[1]])}"/>
                                    <span class="dash">-</span>
                                    <input class="datebox"
                                           value="{format(selection[1], 'hh:mm aa')}"
                                           on:change="{(e)=>updateSelection(currentDate,
                                                      i,
                                                      [selection[0],
                                                      parseByTime(currentDate, e.target.value)])}"/>
                                    
                                </span>
                                <span class="selection-action">
                                    <i class="fa-solid fa-xmark selection-cancel"
                                       on:click="{()=>removeSelection(currentDate, i)}"/>
                                </span>
                            </div>
                        {/each}
                    {/if}
                    <Button block on:click="{()=>insertSelection(currentDate, [currentDate, currentDate])}">
                        <i class="icon fa-solid fa-plus" />
                        {strings.DATETIMERANGEPICKER_ADD_TIME}
                    </Button>
                </div>
            {:else}
                <div class="date-subtitle">
                    {strings.DATETIMERANGEPICKER_SELECT_DATE}
                </div>
            {/if}
        </div>
</div>

<style>
    .button-container {
        margin-top: 5px;
    }

    .icon {
        color: var(--accent);
        padding-right: 5px;
    }
    .wrapper {
        display: flex;
        border-radius: 3px;
        border-color: var(--accent);
        height: 450px;
    }

    .selecter {
        margin: 10px;
        width: 100%;
        max-width: 370px;
    }

    .datebox {
        max-width: 110px;
        text-align: center;
        border-radius: 3px;
        border: 1px solid var(--tertiary);
        margin: 0 5px;
        padding: 5px 15px;
    }

    .date-subtitle {
        padding-top: 10px;
        color: var(--secondary);
        font-size: 13px;
        font-weight: 600;
    }

    .selection {
        padding: 3px;
        margin: 10px 0px;
        border-radius: 4px;
        font-size: 15px;
        display: flex;
        max-width: 370px;
    }

    .selection-content {
        display: flex;
        width: 100%;
        transform: translateX(-5px);
        align-items: center;
    }

    .selection-action {
        float: right;
        margin-right: 10px;
    }

    .selection-cancel {
        color: var(--accent);
        cursor: pointer;
        opacity: 0.5;
        transition: opacity 0.5s;
        transform: translateY(5px);
    }

    .selection-cancel:hover {
        opacity: 1;
    }
</style>

