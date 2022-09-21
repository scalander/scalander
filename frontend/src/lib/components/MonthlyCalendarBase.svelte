<script>
  // components
  import Button from "./ui/Button.svelte";
  import DateButton from "./ui/DateButton.svelte";

  // dating helper
  // oh wait
  import { calendarPaddingHelper } from "./calengine";

  // Weeks Start on Sunday, right?
  // right, North America? booo
  export let mondayweeks = false;

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

</script>

<div class="calendar-container">
  <div class="calendar-metadata-container">
    <div class="year">{year}</div>
    <div class="month">{month}</div>
  </div>
  <div class="calendar-buttons">
    <Button on:click="{decrementMonth}">-</Button>
    <Button on:click="{incrementMonth}">+</Button>
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
      <DateButton primary color="var(--secondary)">{day.getDate()}</DateButton>
    {/each}
    {#each endPadding as day}
      <DateButton color="var(--background-contrast)"
                   on:click="{incrementMonth}">{day.getDate()}</DateButton>
    {/each}
  </div>
</div>



<style>
  .calendar {
      /* in case you haven't picked it up by now
       calendars are usually a grid */
      display: grid;

      /* there are seven days in a week */
      /* 4 weeks + 2 weeks padding = 6 weeks */
      grid-template-columns: repeat(7, 14%);
      grid-template-rows: 10% repeat(5, 18%);

      /* Set the width */
      width: 300px;
      height: 300px;
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
       }

       .year {
           display: inline;
       }

       .month {
           display: inline;
       }

       .calendar-buttons {
           display: inline;
       }

       
</style>
