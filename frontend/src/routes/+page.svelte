<script>
  let testaroo = [1,2,3,4,5];  
  let result = "";
  $: console.log(result);
</script>


{#each testaroo as test (test)}
  <!-- Only do odd numbers. -->
  <div style="cursor:pointer" on:click="{()=>testaroo= [...testaroo, test+1]}">test! {test} {result}</div>
{/each}
<input placeholder="hewo" bind:value="{result}">
