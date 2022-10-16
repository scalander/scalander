function calendarPaddingHelper(month, year, mondayWeeks = false) {
  // Calculate when weeks start and end
  // note in JS dates SUNDAY is 0 and SATURDAY is 6
  const weekStartDay = mondayWeeks ? 1 : 0;
  // day #7 doesn't exist, but it shall now to
  // make subtraction work
  const weekEndDay = mondayWeeks ? 7 : 6;

  // Calculate the first day of this month
  // month-1 becasue month 0 is Janurary but day 0
  // is the previous month's last day go figure
  // I love JS.
  const firstDay = new Date(year, month-1, 1, 0,0,0,0);
  const lastDay = new Date(year, month, 0, 0,0,0,0);

  // get number of days in a month
  const daysBetween = lastDay.getDate() - firstDay.getDate();

  // And subsequently, calculate the number of days
  // of padding to add
  // for some godaweful reason, again, weeks start at 0
  // so we will check if we have -1 (its a sunday), and
  // if so provide 6 days of padding
  const beginPadding_ = firstDay.getDay() - weekStartDay;
  const beginPadding = beginPadding_ == -1 ? 6 : beginPadding_;
  // given we made a fictional day 7, we may create
  // an entire 7 days of padding. We therefore check that
  // and remove it before declaring the final variable
  const endPadding_ = weekEndDay-lastDay.getDay();
  const endPadding = endPadding_ == 7 ? 0 : endPadding_;

  // calculatte the begin padding days
  const today = new Date();
  // get early padding dates
  let beginPaddingDates = [];
  // search forward and prepend
  // plus one because TODO we have an off-by-one error
  for (let pad = -1; -pad < beginPadding+1; pad--) {
    const newDate = new Date(firstDay.getFullYear(),
                             firstDay.getMonth(),
                             firstDay.getDate()+pad);
    beginPaddingDates = [newDate, ...beginPaddingDates];
  }
  // end padding dates
  let endPaddingDates = [];
  // search forward and prepend
  // plus one because TODO we have an off-by-one error
  for (let pad = endPadding; pad != 0; pad--) {
    const newDate = new Date(lastDay.getFullYear(),
                             lastDay.getMonth(),
                             lastDay.getDate()+pad);
    endPaddingDates = [newDate, ...endPaddingDates];
  }

  // Get dates in the middle
  let middleDates = [firstDay];

  // we don't care about hours, we are just going to compare
  // the DATE instead of exact date object
  while (middleDates[middleDates.length-1].getDate() != lastDay.getDate()) {
    middleDates.push((new Date(year,
                              middleDates[middleDates.length-1].getMonth(),
                               middleDates[middleDates.length-1].getDate()+1)));
  }

  return [beginPaddingDates, middleDates, endPaddingDates];
}

function getGapsStartRangesArray(start, end, ranges=[]) {
    // we will use a greedy search algorithum to inch
    // forward until we satisfy ranges until end date
    // ASSUMPTION: ranges is assorted by start time
    
    // tally for found chunks
    let chunks = [];

    // create the "current time"
    // it start at the start, we will essentially
    let epoch = start;

    // while we have not finished consuming the entire
    // range, we keep popping from the front
    while (ranges.length > 0) {
        // current meeting (earliest)
        let current_range = ranges.shift();

        // if the epoch (current time) is BEFORE
        // the start, then we have a chunk that
        // ends at the start
        if (epoch < current_range.start) {
            chunks.push({
                start: epoch,
                end: current_range.start
            });
        }

        // we then move epoch forward to the end of
        // the range in question
        epoch = current_range.end;
    }

    return chunks;
}

function freebusyHelper(freebusy, calChoices=[]) {
    // helper to calculate freebusy info based on calendar choices

    // optionally filter by calChoices
    if (calChoices.length > 0) {
        // TODO refactor but basicaly this is a dictionary filter
        freebusy = Object.fromEntries(Object.entries(freebusy).filter(([k,v]) => calChoices.includes(v.calendar_name)));
    }

    // create an array to tally all busy info
    let global_busy = [];

    // get busy info for every calendar
    for (const [_,v] of Object.entries(freebusy)) {
        // get the ranges for which the user is busy
        let busy_info = v.busy;
        // convert all the dates to unix time (ms)
        busy_info = busy_info.map(i=>({start: new Date(i.start),
                                       end: new Date(i.end)}));

        Object.fromEntries(Object.entries(freebusy).map(([k,v]) =>
            [k, new Date(v).getTime()])); // cast each entry to Unix time
        // tally
        global_busy = [...global_busy, ...busy_info];
    }
    // sort by start
    global_busy.sort((x,y)=>(x.start>y.start));
    
    // create today and 60 days from now
    // TODO perhaps make this not hard-coded? but given the DB
    // hard codes 60 days, I think this is fine
    let start_date = new Date();
    let end_date = new Date(start_date.getFullYear(),
                            start_date.getMonth(),
                            start_date.getDate()+60);

    // get gaps
    let gaps = getGapsStartRangesArray(start_date.getTime(),
                                       end_date.getTime(),
                                       global_busy);

    // serialize gaps and return
    return gaps.map(i=>[new Date(i.start),
                        new Date(i.end)]);
}


export { calendarPaddingHelper,freebusyHelper };


