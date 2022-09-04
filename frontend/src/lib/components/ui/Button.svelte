<script>
  // spring!
  import { spring } from "svelte/motion";

  // Prop to declare whether or not the button
  // is the active or passive style 
  export let primary = false;

  // Color props. By default they are the main accent
  export let color = "var(--accent)";
  export let contrastColor = "var(--accent-contrast)";

  // Primary color mappings
  $: border=color;
  $: backgroundColor = primary?color:"inherit";
  $: color_ = primary?contrastColor:color; 
</script>

<div on:click
     class="button"
     style:border-color="{border}"
     style:color="{color_}"
     style:background-color="{backgroundColor}">
  <slot />
</div>

<style>

  div {
    /* disable blue highlight when tapped multiple times*/
    /* Remember again that this is component scoped */
    cursor: pointer;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    outline:0;

    /* Inline display */
    display: inline-block;
  }

  /* styling actually relating to button goes here */
  .button {
    /* borders! */
    border-radius: 3px;
    border-width: 2px; 
    padding: 1px 2px;

    /* texts! */
    font-weight: 600;
  }
</style>


