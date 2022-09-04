<script>
  import Button from "./ui/Button.svelte";
  import DateButton from "./ui/DateButton.svelte";

  // Weeks Start on Sunday, right?
  // right, North America? booo
  export let mondayweeks = false;

  // Calculate when weeks start and end
  // note in JS dates SUNDAY is 0 and SATURDAY is 6
  const weekStartDay = mondayweeks ? 1 : 0;
  // day #7 doesn't exist, but it shall now to
  // make subtraction work
  const weekEndDay = mondayweeks ? 7 : 6;

  // Abbrev. names for the days of the week
  // Monday first because correctness TODO
  // this is for localization
  const daysOfWeek = ["Mon", "Tues",
                      "Wed", "Thu",
                      "Fri", "Sat", "Sun"];

  // Get an origin month and year
  export let month = 3;
  export let year = 2022;

  // Calculate the first day of this month
  // month-1 becasue month 0 is Janurary but day 0
  // is the previous month's last day go figure
  // I love JS.
  const firstDay = new Date(year, month-1, 1, 0,0,0,0);
  const lastDay = new Date(year, month, 0, 0,0,0,0);

  // And subsequently, calculate the number of days
  // of padding to add
  // for some godaweful reason, again, weeks start at 0
  // so we will check if we have -1 (its a sunday), and
  // if so provide 6 days of padding
  let beginPadding_ = firstDay.getDay() - weekStartDay;
  const beginPadding = beginPadding_ == -1 ? 6 : beginPadding_;
  // given we made a fictional day 7, we may create
  // an entire 7 days of padding. We therefore check that
  // and remove it before declaring the final variable
  let endPadding_ = weekEndDay-lastDay.getDay();
  const endPadding = endPadding_ == 7 ? 0 : endPadding_;
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
