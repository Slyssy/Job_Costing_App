// Bar Chart for Est. labor expense vs actual labor expense
console.log("Hello")
console.log(project_list)

projectArray = Object.keys(project_list).map(i => project_list[i])
console.log(projectArray)

// function buildPlot(data){

//   for (const item in data) {
//     est_labor = []

//     est_labor.push(data[item].fin_est_labor_expense)
//   }

//   for (const item in data) {
//     act_labor = []

//     act_labor.push(data[item].fin_act_labor_expense)
//   }

//   console.log(est_labor)
//   console.log(act_labor)

  var trace1 = {
    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    y: est_labor,
    type: 'bar',
    name: 'Estimated Labor Expense',
    marker: {
     color: 'rgb(49,130,189)',
     opacity: 0.7,
    }
   }

  var trace2 = {
    x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    y: act_labor,
    type: 'bar',
    name: 'Actual Labor Expense',
    marker: {
      color: 'rgb(204,204,204)',
      opacity: 0.3
    }
    };

  var data = [trace1, trace2];

  var layout = {
    title: 'January 2020 Through December 2020',
    xaxis: {
     tickangle: -45
    },
    barmode: 'group'
  };

  Plotly.newPlot('time_series', data, layout)


buildPlot(project_list)