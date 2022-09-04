<script>
  import Button from "./ui/Button.svelte";
  let num = 0;
</script>

<Button on:click="{()=>num += 1}"/>
{num}


