import React from "react";
import { DateRangePicker } from "rsuite";

const DateRange = ({ setStartDate, setEndDate, startedDate }) => {
  const handleDateChange = (value) => {
    if (value) {
      const [startDate, endDate] = value;

      const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0"); // 01-12
        const day = String(date.getDate()).padStart(2, "0"); // 01-31

        return `${year}-${month}-${day}`;
      };
      setStartDate(formatDate(startDate));
      setEndDate(formatDate(endDate));

      console.log("Start:", formatDate(startDate));
      console.log("End:", formatDate(endDate));
      console.log(startedDate);
    }
  };

  return (
    <div>
      <DateRangePicker
        style={{ width: "200px" }}
        showOneCalendar
        size="lg"
        format="dd-MM-yyyy"
        placeholder="Select Date Range"
        onChange={handleDateChange}
      />
    </div>
  );
};

export default DateRange;