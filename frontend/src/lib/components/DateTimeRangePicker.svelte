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
                    {format(selection[0], "HH:mm aa")} — {format(selection[1], "HH:mm aa")}
                  </span>
                  <span class="selection-action">
                    <i class="fa-solid fa-xmark selection-cancel"
                       on:click="{()=>removeSelection(currentDate, selection)}"/>
                  </span>
                </div>
              {/each}
            {/if}
            <Button block><i class="icon fa-solid fa-plus" />{strings.DATETIMERANGEPICKER_ADD_TIME}</Button>
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

  

  .date-subtitle {
      padding-top: 10px;
      color: var(--secondary);
      font-size: 13px;
      font-weight: 600;
  }

.selection {
      padding: 5px;
      margin: 10px 0px;
      border: 0.5px solid var(--secondary);
      border-radius: 4px;
      font-weight: 600;
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
  }

  .selection-cancel:hover {
      opacity: 1;
  }
</style>

