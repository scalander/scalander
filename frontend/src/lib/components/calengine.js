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

// https://stackoverflow.com/questions/39469064/find-holes-gaps-in-array-of-date-ranges
function getGapsStartRangesArray(start, end, ranges) {
    let chunks = [],
        i = 0, len = ranges.length, range;

    let _start = start;

    // If there are no ranges cached, create one big chunk for entire range.
    if (!len) {
        chunks.push({start: start, end: end});
    } else {

        for (; i < len; i++) {
            range = ranges[i];

            // Cache is complete or start is higher then end, we can stop looping
            if (range.start >= end || (range.start <= start && range.end >= end)) {
                _start = end;
                break;
            }

            // Range hasn't gotten to start date yet, so continue
            if (range.end < start)
                continue;

            // This range is lower then the current _start time, so we can go ahead to its end time
            if (range.start <= _start) {
                _start = range.end;
            }
            // This range is higher then the current _start time, so we are missing a piece
            else {
                console.log('missing piece', new Date(_start), new Date(range.start));
                chunks.push({
                    start: _start,
                    end: range.start
                });
                _start = range.end;
            }
        }

        // Final piece (if required)
        if (_start < end) {
            chunks.push({
                start: _start,
                end: end
            });
        }
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
        busy_info = Object.fromEntries(Object.entries(freebusy).map(([k,v]) =>
            [k, new Date(v).getTime()])); // cast each entry to Unix time
        // tally
        global_busy = global_busy+busy_info;
    }
    // sort by start
    global_busy.sort(x=>x.start);
    
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
    return gaps.map(i=>[new Date(i.start()),
                        new Date(i.end())]);
}


export { calendarPaddingHelper,freebusyHelper };


