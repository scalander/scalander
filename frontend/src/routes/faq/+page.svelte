<script>
    import strings from "$lib/strings.json";
</script>
<div id="content">

    <h1>{strings.FAQ_TITLE}</h1><br><br>


    <h2>{strings.FAQ_ONE}</h2>
    <p>{strings.FAQ_ONE_ANSWER}</p><br>

    <h2>{strings.FAQ_TWO}</h2>
    <p>{strings.FAQ_TWO_ANSWER}</p><br>

    <h2>{strings.FAQ_THREE}</h2>
    <p>{strings.FAQ_THREE_ANSWER}</p><br>

    <h2>{strings.FAQ_FOUR}</h2>
    <p>{strings.FAQ_FOUR_ANSWER}</p><br>
    <!--ADD MORE IF NEEDED-->

    <br><br><br>
    <h2>{strings.FAQ_CONTACT_HEADER}</h2>
    <p>{strings.FAQ_CONTACT_INFO} <a href="https://github.com/scalander/scalander/tree/main">GitHub</a>.</p>
</div>
<style>

    h1 {
        font-weight: 700;
        color: var(--accent);
        font-size: 30px;
    }


    h2 {
        font-weight: 600;
        color: var(--accent);
        font-size: 20px;
        margin-top: 10px;
    }

    /* h3 {
        margin-top: 10px;
    }

    p,ul {
        font-weight: 500;
        font-size: 15px;
    }

    ul {
        list-style-type: disc;
    }

    li {
        margin-left: 15px;
    } */

    a {
        color: var(--blue);
    }

    /* a { */
    /*     color: var(--accent); */
    /* } */

    #content {
        margin: 20px;
    }

</style>