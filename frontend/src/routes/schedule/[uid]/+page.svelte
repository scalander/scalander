<svelte:head>
    <script src="https://accounts.google.com/gsi/client"></script>
</svelte:head>


<script>
    // the date picker
    import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"

    // page info
    import { page } from '$app/stores';

    // current changes
    let change = []
    import { onMount } from 'svelte';

    // the button
    let gbutton;

    onMount(()=>{
        google.accounts.id.initialize({
            client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
            callback: ()=>{}
        });
        google.accounts.id.renderButton(
            gbutton,
            { size: "large",
              width: 100 } 
        );

    });


</script>

<!-- UID: {$page.params.uid} -->


<span bind:this={gbutton} id="gbutton"/>

<div>test</div>

<DateTimeRangePicker on:change="{(e)=> change=e.detail.selected}"/>





<style>
    #button * {
        display: inline;
        width: 0%;
    }
</style>
