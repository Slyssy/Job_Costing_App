// Bar Chart for Est. labor expense vs actual labor expense
console.log("Hello");
console.log(project_list);

projectArray = Object.keys(project_list).map((i) => project_list[i]);
console.log(projectArray);

function buildPlot(data) {
  project_names = [];

  for (const item in data) {
    project_names.push(data[item].project_name);
  }

  est_labor_exp = [];

  for (const item in data) {
    est_labor_exp.push(data[item].fin_est_labor_expense);
  }

  act_labor_exp = [];

  for (const item in data) {
    act_labor_exp.push(data[item].fin_act_labor_expense);
  }

  est_hours = [];

  for (const item in data) {
    est_hours.push(data[item].fin_est_labor_hours);
  }

  act_hours = [];

  for (const item in data) {
    act_hours.push(data[item].fin_act_labor_hours);
  }

  dates = [];

  for (const item in data) {
    dates.push(data[item].act_start_date);
  }

  var trace1 = {
    x: dates,
    y: est_hours,
    type: "bar",
    name: "January 2020 Through December 2020",
    marker: {
      color: "rgb(49,130,189)",
      opacity: 0.7,
    },
  };
  var trace2 = {
    x: dates,
    y: act_hours,
    type: "bar",
    name: "Actual Hours",
    marker: {
      color: "rgb(204,204,204)",
      opacity: 0.5,
    },
  };
  var data = [trace1, trace2];

  var layout = {
    title: "January 2020 Through December 2020",
    xaxis: {
      tickangle: -45,
    },
    barmode: "group",
  };

  Plotly.newPlot("time_series", data, layout);
}

buildPlot(project_list);
