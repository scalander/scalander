<script>
  // calendar
  import MonthlyCalendarBase from "./MonthlyCalendarBase.svelte";
  import Button from "./ui/Button.svelte";

  // crono
  import * as chrono from 'chrono-node';

  // date formatting
  import { format } from 'date-fns'

  // currently selected times
  let selected = {
  };

  let tmp1 = new Date(2022, 9, 17);
  let tmp2 = [[new Date(2022, 9, 17, 9, 3, 22),
               new Date(2022, 9, 17, 10, 3, 22)]];

  selected[tmp1] = tmp2;

  
  // currently selected date
  let currentDate = null;

  // strings
  import strings from "$lib/strings.json";

  // function to remove a selection
  function removeSelection(date, selection) {
    let currentSelections = selected[date];
    // filter for current selection
    currentSelections = currentSelections.filter(i=>i!=selection);
    // set it back
    selected[date] = currentSelections;
  }

  // function to insert a selection
  function insertSelection(date, newSelection) {
    // get selections
    let currentSelections = selected[date] ? selected[date] : [];
    // append
    currentSelections.push(newSelection);
    // put it back
    selected[date] = currentSelections;
  }

  // function to update a selection
  function updateSelection(date, oldSelection, newSelection) {
    let currentSelections = selected[date];
    // filter for current selection
    currentSelections = currentSelections.filter(i=>i!=oldSelection);
    // append
    currentSelections.push(newSelection);
    // put it back
    selected[date] = currentSelections;
  }

  // function to parse and update time
  function parseByTime(refDate, timeStr) {
    // run chrono
    let date = chrono.parseDate(timeStr);
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
  <MonthlyCalendarBase on:select={(e)=>
    currentDate = e.detail.date} />
    <div class="selecter">
      {#if currentDate}
        <div class="date-subtitle">
          {strings.DATETIMERANGEPICKER_SELECTING_TIME.replace("$DATE",
                        format(currentDate, "EEEE, MMMM dd, yyyy"))}
        </div>
        <div class="button-container">
            {#if selected[currentDate]}
              {#each selected[currentDate] as selection}
                <div class="selection">
                  <span class="selection-content">
                    <input class="datebox"
                           value="{format(selection[0], 'hh:mm aa')}"
                           on:change="{(e)=>updateSelection(currentDate,
                                      selection,
                                      [parseByTime(currentDate, e.target.value),
                                       selection[1]])}"/>
                    <span class="dash">-</span>
                    <input class="datebox"
                           value="{format(selection[1], 'hh:mm aa')}"
                           on:change="{(e)=>updateSelection(currentDate,
                                      selection,
                                      [selection[0],
                                      parseByTime(currentDate, e.target.value)])}"/>
                  </span>
                  <span class="selection-action">
                    <i class="fa-solid fa-xmark selection-cancel"
                       on:click="{()=>removeSelection(currentDate, selection)}"/>
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

