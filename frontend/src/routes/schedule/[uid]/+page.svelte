<script>
  const CLIENT_ID_TODO="966652940331-g1ld879a9gn25rk39dhta87u0trjasp3.apps.googleusercontent.com";
  // the date picker
  // import DateTimeRangePicker from "$lib/components/DateTimeRangePicker.svelte"

  // page info
  // import { page } from '$app/stores';

  // current changes
  // let change = []
  import { onMount } from 'svelte';

  onMount(()=>{
    window.onload = function () {
      console.log("test!!");
      google.accounts.id.initialize({
        client_id: '966652940331-g1ld879a9gn25rk39dhta87u0trjasp3.apps.googleusercontent.com',
        callback: ()=>{}
      });
      google.accounts.id.renderButton(
        document.getElementById("buttonDiv"),
        { size: "small" } 
      );

    };
  });


  // onMount(async () => {
  //   console.log("hewo");
  // });


</script>
<svelte:head>
  <script src="https://accounts.google.com/gsi/client"
          async
          defer></script>
</svelte:head>


<!-- UID: {$page.params.uid} -->


<div id="buttonDiv" style:background="transparent"/>

<!-- <div id="g_id_onload" -->
<!--      data-client_id="{CLIENT_ID_TODO}" -->
<!--      data-auto_prompt="false"> -->
  <!-- </div> -->
<!-- <div class="g_id_signin" -->
<!--      data-type="standard" -->
<!--      data-size="large" -->
<!--      data-theme="outline" -->
<!--      data-text="sign_in_with" -->
<!--      data-shape="rectangular" -->
<!--      data-logo_alignment="left"> -->
  <!-- </div> -->
<!-- data-callback="test" -->
<!-- <div id="g_id_onload" -->
<!--      data-client_id="966652940331-g1ld879a9gn25rk39dhta87u0trjasp3.apps.googleusercontent.com" -->
<!--      data-context="signin" -->
<!--      data-ux_mode="popup" -->
<!--      data-itp_support="true" -->
<!--      data-auto_prompt="false"> -->
  <!-- </div> -->

<!-- <div class="g_id_signin" -->
<!--      data-type="standard" -->
<!--      data-shape="rectangular" -->
<!--      data-theme="outline" -->
<!--      data-text="signin_with" -->
<!--      data-size="large" -->
<!--      data-logo_alignment="left"> -->
  <!-- </div> -->


<!-- <DateTimeRangePicker on:change="{(e)=> change=e.detail.selected}"/> -->

<!-- {change} -->




  <style>
    .L5Fo6c-bF1uUb {
        display: none;
    }
    </style>
