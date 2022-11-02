<script>
    // strings
    import strings from "$lib/strings.json";

    // import button!
    import Button from '$lib/components/ui/Button.svelte';
</script>

<div id="header">
    <h1>Scalander</h1>
</div>

<div id="background">
    &nbsp;
</div>

<div id="center-clearfix">
    <div id="center">
        <!-- hard coded string because its the darn app's name -->
        <h2 class="callout">{strings.HOMEPAGE_CALLOUT}</h2>
        <p class="callout-text">{strings.HOMEPAGE_DESCRIPTION}</p>
        <br />
        <a href="./create"><Button primary>{strings.HOMEPAGE_BUTTON}</Button></a>
        <a href="/privacy" class="link">Privacy</a>
        <a href="/terms" class="link">Terms</a>
    </div>
</div>
<div id="copyright">©2022 Scalander and various open source contributors. 131 E. 28th Ave., San Mateo, California 94403. All rights reserved except where prohibited by applicable law.</div>




<style>

    #header {
        width: 100%;
        float: top;
        height: 50px;
        padding: 10px;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    h1 {
        font-weight: 700;
        color: var(--accent);
        font-size: 25px;
        font-style: italic;
    }

    .callout {
        color: var(--accent);
        font-weight: 700;
        font-size: min(100px, 15vw);
        line-height: 1.3;
        mix-blend-mode: darken;
    }

    .callout-text {
        font-weight: 500;
        font-size: 25px;
    }

    #center-clearfix {
        width: 95vw;
        height: calc(100vh - 50px - 30px); /* for header and footer */
        display: flex;
        justify-content: center;
        align-items: center;
        overflow-x: hidden;
    }

    #background {
        width: 100vw;
        height: 100vh;
        position: absolute;
        background: url("$lib/background.svg");
        z-index: -1;
        background-size: cover;
        opacity: 0.5;
        top:0;
    }

    #center {
        width: min(700px, 90vw);
    }

    .link {
        color: var(--accent);
        float: right;
        padding: 8px 5px 0 5px;
        font-size: 13px;
        font-weight: 600;
    }

    #copyright {
        height: 30px;
        bottom: 5px;
        color: var(--background-contrast);
        font-size: 8px;
        text-align: center;
        margin: 0 auto;
        padding: 10px;
        width: 100%;
    }

</style>
