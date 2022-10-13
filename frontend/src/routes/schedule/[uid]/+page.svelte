<svelte:head>
  <script src="https://accounts.google.com/gsi/client"></script>
</svelte:head>


<script>
  const CLIENT_ID_TODO="966652940331-g1ld879a9gn25rk39dhta87u0trjasp3.apps.googleusercontent.com";
  // the date picker
  import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"

  // page info
  import { page } from '$app/stores';

  // current changes
  let change = []
  import { onMount } from 'svelte';

  // the button
  let button;

  onMount(()=>{
    google.accounts.id.initialize({
      client_id: '966652940331-g1ld879a9gn25rk39dhta87u0trjasp3.apps.googleusercontent.com',
      callback: ()=>{}
    });
    google.accounts.id.renderButton(
      button,
      { size: "large",
        width: 100 } 
    );

  });


</script>

<!-- UID: {$page.params.uid} -->


<span bind:this={button} id="button"/>

<div>test</div>

<DateTimeRangePicker on:change="{(e)=> change=e.detail.selected}"/>





<style>
  #button * {
      display: inline;
      width: 0%;
  }
</style>
