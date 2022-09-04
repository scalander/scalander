<script>
  import Button from "./ui/Button.svelte";
  let num = 0;
</script>

<div class="m-4">
  <Button on:click="{()=>num += 1}" color="var(--blue)">Groot!</Button>
  <Button on:click="{()=>num += 1}" primary>Groot!</Button>
  <Button on:click="{()=>num += 1}" color="var(--green)" contrastColor="var(--black)" primary>Groot!</Button>
</div>
{num}


