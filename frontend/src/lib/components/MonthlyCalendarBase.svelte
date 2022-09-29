<script>
  // components
  import Button from "./ui/Button.svelte";
  import DateButton from "./ui/DateButton.svelte";

  // event dispatching
  import { createEventDispatcher } from 'svelte';

  // dating helper
  // oh wait
  import { format, isSameDay } from 'date-fns'; 
  import { calendarPaddingHelper } from "./calengine";

  // dispatcher
  const dispatch = createEventDispatcher();

  // Weeks Start on Sunday, right?
  // right, North America? booo
  export let mondayweeks = false;

  // set current selection
  let selection = null;

  // get today
  const today = new Date();

  // get seed date
  export let month = today.getMonth()+1;
  export let year = today.getFullYear();

  // Abbrev. names for the days of the week
  // Monday first because correctness TODO
  // this is for localization
  let daysOfWeek = ["Mon", "Tues",
                    "Wed", "Thu",
                    "Fri", "Sat", "Sun"];
  // if we are for some godforsaken reason
  // Sunday first, we pop the sunday to the front
  if (!mondayweeks)
    daysOfWeek = [daysOfWeek.pop(0), ...daysOfWeek];

  $: [beginPadding, middleDates, endPadding] = calendarPaddingHelper(month, year, mondayweeks);

  // functions to increment and decrement months
  function incrementMonth() {
    // get the active month
    // again, months start from 0, and we set
    // date to 32 to get the NEXT month
    let active = new Date(year, month-1, 32)
    month = active.getMonth()+1; // add month by 1 to solve 0
    year = active.getFullYear(); // add month by 1 to solve 0
  }
  function decrementMonth() {
    // get the active month
    // again, months start from 0, and we set
    // date to 0 to get the PREVIOUS month
    let active = new Date(year, month-1, 0)
    month = active.getMonth()+1; // add month by 1 to solve 0
    year = active.getFullYear(); // add month by 1 to solve 0
  }

  // function to send ping
  function select(date) {
    // if the date is not selected, select it
    if (selection != date) {
      selection = date;
      dispatch('select', {date});
    // otherwise, deselect it
    } else {
      selection = null;
      dispatch('select', {date: null});
    }
  }

  // function to reset dates to home
  function reset() {
    month = today.getMonth()+1;
    year = today.getFullYear();
  }

</script>

<div class="calendar-container">
  <div class="calendar-metadata-container" on:click="{reset}">
    <div class="year">{year}</div>
    <!-- TODO localization -->
    <div class="month">{format(new Date(year, month, 0), "LLLL")}</div>
  </div>
  <div class="calendar-buttons">
    <span class="calendar-button left-button" on:click="{decrementMonth}">
      <i class="fa-solid fa-caret-left" /></span>
    <span class="calendar-button right-button" on:click="{incrementMonth}">
      <i class="fa-solid fa-caret-right" /></span>
  </div>

  <div class="calendar m-4">
    {#each daysOfWeek as day}
      <div class="header-item">{day}</div>
    {/each}
    {#each beginPadding as day}
      <DateButton color="var(--background-contrast)"
                  on:click="{decrementMonth}">{day.getDate()}</DateButton>
    {/each}
    {#each middleDates as day}
    <!-- we put an inverse operation here, because we could -->
    <!-- like to invert the color when its today -->
      <div>
        <DateButton
          on:click="{()=>{select(day)}}"
          color="var(--tertiary)"
          contrastColor="var(--tertiary-contrast)"
          primary
          inverse="{isSameDay(day, new Date())}">{day.getDate()}</DateButton>
        {#if day == selection}
            <i class="highlighted-dot fa-solid fa-circle" />
        {/if}
      </div>
    {/each}
    {#each endPadding as day}
        <DateButton color="var(--background-contrast)"
                    on:click="{incrementMonth}">{day.getDate()}</DateButton>
    {/each}
    </div>
</div>



<style>
  /* set the width and height for the master object */
  .calendar-container {
      /* Set the width and height */
      width: 300px;
      height: 300px;
  }

  .calendar {
      /* in case you haven't picked it up by now
       calendars are usually a grid */
      display: grid;

      /* there are seven days in a week */
      /* 4 weeks + 2 weeks padding = 6 weeks */
      grid-template-columns: repeat(7, 14%);
      grid-template-rows: 10% repeat(5, 18%);

      /* Set the width and height */
      width: 300px;
      height: 300px;

      /* set margin */
      margin: 0;
      }

       .header-item {
           /* The top should be unremarkable */
           color: var(--secondary);
           /* and small */
           font-size: 13px;
           /* centering */
           display: flex;
           justify-content: center;
           align-items: center;
           /* slightly shift to the left for Jack's asthetic preferences */
           transform: translateX(-4px);
  }

  .calendar-metadata-container {
      display: inline;
      cursor: pointer;
  }

  .calendar-buttons {
      float: right;
      padding-right: 10px;
      cursor: pointer;
  }

  .year {
      display: inline;
      font-weight: 600;
      color: var(--primary);
  }

  .month {
      display: inline;
      font-size: 30px;
      font-weight: 600;
      color: var(--accent);
  }

  .calendar-buttons {
      display: inline;
      transform: translateY(10px);
  }

  .highlighted-dot {
      font-size: 6px !important;
      transform: translateY(-9px) translateX(6px);
      background: transparent;
  }

  i {
      padding: 10px;
      font-size: 20px;
      color: var(--accent);
  }

  
</style>
