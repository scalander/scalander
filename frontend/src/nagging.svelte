<script>
let invitedUsers = [{
    name: "bob",
},
{
    name: "joe"
}] //invited people - currently hardcoded as a placeholder


let proposals = [{
    start: 1663794021, // proposed start time
    end: 1663798021, // proposed end time
    commitedUsers: [UserMeetingSubscription], // commited users
    unavailableUsers: [UserMeetingSubscription], // to nag users
    optimality: int // 0 means the best solution
}]


let meeting = { //currently filled with placeholders - eventually we'll take this in
    name: "talk about beans",
    start: 1663794021, // possible RANGE start as a Unix timestamp hardcoded as a placeholder
    end: 1663994021, // possible RANGE end as a Unix timestamp hardcoded as a placeholder
    proposals: [MeetingTimeProposal],
    subscribedUsers: [UserMeetingSubscription],
    lockInDate: Date, // after this date, meeting can't be rescheduled
}

</script>

<main>



</main>