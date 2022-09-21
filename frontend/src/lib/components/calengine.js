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
  for (let pad = 1; pad < endPadding+1; pad++) {
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

export { calendarPaddingHelper };


