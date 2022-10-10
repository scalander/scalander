<script>
  import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"
  import { page } from '$app/stores';

  let change = [];
</script>

UID: {$page.params.uid}

<DateTimeRangePicker on:change="{(e)=> change=e.detail.selected}"/>

{change}



