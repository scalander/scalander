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

  // Get an origin month and year
  export let month = 3;
  export let year = 2022;

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

  const [beginPadding, endPadding] = calendarPaddingHelper(month, year, mondayweeks);


</script>

<div class="calendar m-4">
  {#each daysOfWeek as day}
    <div class="header-item">{day}</div>
  {/each}
  <DateButton>9</DateButton>
  <DateButton>10</DateButton>
  <DateButton color="var(--orange)">11</DateButton>
  <DateButton>12</DateButton>
  <DateButton primary>13</DateButton>
  <DateButton>14</DateButton>
</div>

{beginPadding}+{firstDay}
<br />
{lastDay}+{endPadding}

<br />
{daysBetween}



<style>
  .calendar {
    /* in case you haven't picked it up by now
       calendars are usually a grid */
    display: grid;

    /* there are seven days in a week */
    /* 4 weeks + 2 weeks padding = 6 weeks */
    grid-template-columns: repeat(7, 14%);
    grid-template-rows: repeat(6, 16%);
    }

     .header-item {
       /* The top should be unremarkable */
       color: var(--secondary);
       /* and small */
       font-size: 13px;
       /* and centered */
       text-align: center;
     }
</style>
