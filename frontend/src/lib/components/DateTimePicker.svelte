<script>
  import Button from "./ui/Button.svelte";
  import DateButton from "./ui/DateButton.svelte";
  let num = 0;
</script>

<div class="m-4">
  <Button on:click="{()=>num += 1}" color="var(--blue)">Groot!</Button>
  <Button on:click="{()=>num += 1}" primary>Groot!</Button>
  <Button on:click="{()=>num += 1}" color="var(--green)" contrastColor="var(--black)" primary>Groot!</Button>



  <DateButton on:click="{()=>num += 1}">9</DateButton>
  <DateButton on:click="{()=>num += 1}">10</DateButton>
  <DateButton on:click="{()=>num += 1}" color="var(--orange)">11</DateButton>
  <DateButton on:click="{()=>num += 1}">12</DateButton>
  <DateButton on:click="{()=>num += 1}" primary>13</DateButton>
  <DateButton on:click="{()=>num += 1}">14</DateButton>
</div>
{num}


