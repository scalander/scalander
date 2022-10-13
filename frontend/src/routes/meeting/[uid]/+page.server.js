/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    let meeting = await (await fetch("http://localhost:8082/api/meeting/" + params.uid)).json();
    return {meeting};
}