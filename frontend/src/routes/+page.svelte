<script>
    // strings
    import strings from "$lib/strings.json";

    // import button!
    import Button from '$lib/components/ui/Button.svelte';
</script>

<div id="center-clearfix">
    <div id="center">
        <!-- hard coded string because its the darn app's name -->
        <h1>Scalander</h1>
        <p>{strings.HOMEPAGE_DESCRIPTION}</p>
        <br />
        <a href="./create"><Button primary>{strings.HOMEPAGE_BUTTON}</Button></a>
        <a href="/privacy" class="link">Privacy</a>
        <a href="https://www.gnu.org/licenses/lgpl-3.0.en.html" class="link">Terms</a>
    </div>
</div>




<style>

    h1 {
        font-weight: 700;
        color: var(--accent);
        font-size: 30px;
    }

    #center-clearfix {
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #center {
        width: min(500px, 90vw);
    }

    .link {
        color: var(--accent);
        float: right;
        padding: 8px 5px 0 5px;
        font-size: 13px;
        font-weight: 600;
    }

</style>
