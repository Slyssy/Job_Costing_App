// Estimated Labor Expense vs. Actual Labor Expense
// let keys = Object.keys(project_dict);

// let values = Object.values(project_dict);
// console.log(project_dict)

// let trace1 = {
//   x: ["Bdg. Labor Exp."],
//   y: [values[7]],
//   name: "Budgeted Labor Expense",
//   type: "bar",
//   marker: {
//     color: "rgb(27, 113, 242)",
//     opacity: 0.5,
//   },
// };

// let trace2 = {
//   x: ["Act. Labor Exp."],
//   y: [values[13]],
//   name: "Actual Labor Expense",
//   type: "bar",
//   marker: {
//     color: "rgb(235, 40, 40)",
//     opacity: 0.5,
//   },
// };

// let expData = [trace1, trace2];

// let expLayout = {
//   title: "Estimated vs. Actual Labor Expense",
//   barmode: "group",
//   yaxis: {
//     title: "Labor Expense ($)",
//   },
// };

// Plotly.newPlot("eva_exp_bar", expData, expLayout);

// // Estimated Labor hours vs Actual Labor Hours
// let trace3 = {
//   x: ["Bdg. Labor Hours"],
//   y: [values[5]],
//   name: "Budgeted Labor Hours",
//   type: "bar",
//   marker: {
//     color: "rgb(27, 113, 242)",
//     opacity: 0.5,
//   },
// };

// let trace4 = {
//   x: ["Act. Labor Hours"],
//   y: [values[11]],
//   name: "Actual Labor Hours",
//   type: "bar",
//   marker: {
//     color: "rgb(235, 40, 40)",
//     opacity: 0.5,
//   },
// };

// let hourData = [trace3, trace4];

// let hourLayout = {
//   title: "Estimated vs. Actual Labor Hours",
//   barmode: "group",
//   yaxis: {
//     title: "Labor Hours",
//   },
// };

// Plotly.newPlot("eva_hr_bar", hourData, hourLayout);

// // Estimated Gross Profit vs. Actual Gross Profit
// let trace5 = {
//   x: ["Bdg. Gross Profit"],
//   y: [values[8]],
//   name: "Budgeted Gross Profit",
//   type: "bar",
//   marker: {
//     color: "rgb(27, 113, 242)",
//     opacity: 0.5,
//   },
// };

// let trace6 = {
//   x: ["Act. Gross Profit"],
//   y: [values[14]],
//   name: "Actual Gross Profit",
//   type: "bar",
//   marker: {
//     color: "rgb(235, 40, 40)",
//     opacity: 0.5,
//   },
// };

// let gpData = [trace5, trace6];

// let gpLayout = {
//   title: "Estimated vs. Actual Gross Profit",
//   barmode: "group",
//   yaxis: {
//     title: "Gross Profit",
//   },
// };

// Plotly.newPlot("eva_gp_bar", gpData, gpLayout);



const margin = {top: 70, right: 20, bottom: 70, left: 100},
    width = 1135 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// Setting x Scale
const x = d3.scaleBand()
.rangeRound([0, width], .05)
.padding(0.1);

// Setting y Scale
const y = d3.scaleLinear().range([height, 0]);

// Building xAxis
const xAxis = d3.axisBottom()
    .scale(x)

// Building y Axis
const yAxis = d3.axisLeft()
    .scale(y)
    .ticks(10);

// Appending svg to dashboard.html ("#estimate-to-actual")
const svg = d3.select("#estimate-to-actual").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Parsing through data to pull data needed for bars and x axis
data.forEach(d => {
   d.act_start_date = d.month;
  d.fin_act_labor_expense = +d.fin_act_labor_expense;
});

// Setting domain for x and y scales
  x.domain(data.map(d => d.month));
  y.domain([0, d3.max(data, d => d.fin_est_labor_expense)]); 

  // Appending a group to the svg and adding the x axis to that group.
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis.ticks(null).tickSize(0))

 // Appending a group to the svg and adding the y axis with labels and to that group.
  svg.append("g")
      // .attr("class", "y axis")
      .call(yAxis.ticks(null).tickSize(-width))       
      
// Defining and placing bars
  svg.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", d => d.fin_act_labor_expense < d.fin_est_labor_expense ? '#1b71f2': '#eb2828')
      .attr("class", "bars")
      .attr("x", d => x(d.act_start_date))
      .attr("width", x.bandwidth())
      .attr("y", d => y(d.fin_act_labor_expense))
      .attr("height", d => height - y(d.fin_act_labor_expense))
      .attr("opacity", ".5");
  
// Defining limit lines for estimated labor expense
  svg.selectAll("lines")
      .data(data)
    .enter().append("line")
      .style("fill", 'none')
  		.attr("x1", d => x(d.act_start_date) + x.bandwidth() +5)
      .attr("x2", d => x(d.act_start_date) -5)
   .attr("y1", d => y(+d.fin_est_labor_expense))
      .attr("y2", d => y(+d.fin_est_labor_expense))
  		.style("stroke-dasharray", [6,2])
  		.style("stroke", "#eb2828")
  .style("stroke-width", 3)

// Adding x Axis labels
svg.append ('text')
    .attr("class", 'xAxis')
    .attr("y", 525)
    .attr("x", width/2)
    .attr("fill", "#635f5d")
    .style('font-size', '2.5em')
    .text( "Months")

// Adding y Axis labels
    svg.append('text')
      .attr('class', 'yAxis')
      .attr('y', -55)
      .attr('x', -380)
      .attr('fill', 'black')
      .attr('transform', `rotate(-90)`)
      .attr("fill", "#635f5d")
      .style('font-size', '2.5em')
      .text("Labor Expense ($)");
      
// Adding Title
  svg.append ('text')
      .attr("class", "Title")
      .attr("y", -20)
      .attr("x", 160)
      .attr("fill", "#635f5d")
      .style("font-size", "3.5em")
      .text("Estimate vs. Actual Labor Expense")