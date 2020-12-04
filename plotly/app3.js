function makeplot(){
Plotly.d3.csv("C:\Users\micha\Project-2-Job_Costing_App\plotly\project_details.csv", function(err, rows){

  function unpack(rows, key) {
  return rows.map(function(row) { return row[key]; });
  
}

let trace1 = {
  type: "bar",
  mode: "lines",
  name: 'revenue',
  x: unpack(rows, 'Date'),
  y: unpack(rows, 'revenue'),
  line: {color: '#17BECF'}
}

let trace2 = {
  type: "bar",
  mode: "lines",
  name: 'est_labor_expense',
  x: unpack(rows, 'Date'),
  y: unpack(rows, 'est_labor_expense'),
  line: {color: '#7F7F7F'}
}

let data = [trace1,trace2];

let layout = {
  title: 'Estimate Revenue vs. Estimated Labor Expense',
  xaxis: {
    autorange: true,
    range: ['act_start_date', 'act_comp_date'],
    rangeselector: {buttons: [
        {
          count: 1,
          label: '1m',
          step: 'month',
          stepmode: 'backward'
        },
        {
          count: 6,
          label: '6m',
          step: 'month',
          stepmode: 'backward'
        },
        {step: 'all'}
      ]},
    rangeslider: {range: ['act_start_date', 'act_comp_date']},
    type: 'date'
  },
  yaxis: {
    autorange: true,
    range: [min('revenue'), max('revenue')],
    type: 'linear'
  }
};

Plotly.newPlot('../plotly/app3.js', data, layout);
})}