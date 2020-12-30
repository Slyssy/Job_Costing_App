// const { range } = require("d3");

// const { scaleBand } = require("d3");

// // load the data
// projectArray = Object.keys(project_list).map((i) => project_list[i]);
// console.log(projectArray);

// parsing through data to pull data needed for bar chart
// const data = projectArray.map(({act_start_date, fin_est_labor_expense, fin_act_labor_expense}) => ({act_start_date, fin_est_labor_expense: parseFloat(fin_est_labor_expense), fin_act_labor_expense: parseFloat(fin_act_labor_expense)}));
// console.log(data)
// // grouping all start dates by month
// const mapDayToMonth = data.map(x => ({...x, act_start_date: new Date(x.act_start_date).getMonth()}));
// // console.log(mapDayToMonth)


// // // summing revenue per month by using reduce function
// const sumPerMonth = mapDayToMonth.reduce(function(allDates, date) {
//   if (allDates.some(function(e) {
//       return e.act_start_date === date.act_start_date
//     })) {
//     allDates.filter(function(e) {
//       return e.act_start_date === date.act_start_date
//     })[0].fin_est_labor_expense += +date.fin_est_labor_expense
//   } else {
//     allDates.push({
//       act_start_date: date.act_start_date,
//       fin_est_labor_expense: +date.fin_est_labor_expense,
//       fin_act_labor_expense: +date.fin_act_labor_expense,
//     })
//   }
//   return allDates
// }, []);
// console.log(sumPerMonth)


// // Creating a function to split the date estimated labor
// const mapperEst = single => {
//   let d = single.act_start_date.split('-');
//   let p = Number(single.fin_est_labor_expense);
//   return { year: d[0], month: d[1], fin_est_labor_expense: p };
// }

// // function to group by date 
// const reducerEst = (group, current) => {
//   let i = group.findIndex(single => (single.year == current.year && single.month == current.month));
//   if (i == -1) {
//     return [ ...group, current ];
//   }
//   group[i].fin_est_labor_expense += current.fin_est_labor_expense;
//   return group;
// };

// // calling mapper and reducer function to sum estimated labor expense for each month and year
// const sumPerMonthEst = data.map(mapperEst).reduce(reducerEst, []);

// // sorting sumPerMonthEst object
// sumPerMonthEst.sort((a, b) => a.year.localeCompare(b.year) || a.month - b.month);
// console.log(sumPerMonthEst);

// // create nested object for group d3 plot for estimated labor expense
// const Estimated = {sumPerMonthEst}
// console.log(Estimated)

// // Creating a function to split the date actual labor expense
// const mapperAct = single => {
//   let d = single.act_start_date.split('-');
//   let p = Number(single.fin_act_labor_expense);
//   return { year: d[0], month: d[1], fin_act_labor_expense: p };
// }

// // function to group by date 
// const reducerAct = (group, current) => {
//   let i = group.findIndex(single => (single.year == current.year && single.month == current.month));
//   if (i == -1) {
//     return [ ...group, current ];
//   }
//   group[i].fin_act_labor_expense += current.fin_act_labor_expense;
//   return group;
// };

// // calling mapper and reducer function to sum actual labor expense for each month and year
// const sumPerMonthAct = data.map(mapperAct).reduce(reducerAct, []);

// // sorting sumPerMonthActt object
// sumPerMonthAct.sort((a, b) => a.year.localeCompare(b.year) || a.month - b.month);
// console.log(sumPerMonthAct);

// // create nested object for group d3 plot for actual labor expense
// const Actual = {sumPerMonthAct}
// console.log(Actual)

// // creating an array of nested objects for estimated and actual labor expense for d3 grouped bar chart
// const estimateActual = [{
//   ...Estimated,
//   ...Actual
// }];
// // estimateActual = [Estimated, Actual]
// console.log(estimateActual)
// // renaming values inside object
// // keysMap = {
// //   act_start_date: 0
// // }
// const svgHeight = 600
// const svgWidth = 1135

// const margin = {
//   top: 50,
//   right: 50,
//   bottom: 50,
//   left: 50
// }

// // set chart demensions
// chartHeight = svgHeight - margin.top - margin.bottom
// chartWidth = svgWidth - margin.left - margin.right

// // defining svg and placing it
// const svg = d3.select("#time_series").append("svg")
//   .attr("height", svgHeight)
//   .attr("width", svgWidth)

// // setting up chart group
// const chartG = svg.append("g")
//   .attr("transform", `translate(${margin.left}, ${margin.top})`)

// // setting scales
// const yScale = d3.scaleLinear()
//   // .domain([0, d3.max(sumPerMonthEst.map(d => d.fin_est_labor_expense))])
//   .domain([0, d3.max(sumPerMonth, d => d.fin_est_labor_expense > d.fin_act_labor_expense ? d.fin_est_labor_expense : d.fin_act_labor_expense)])
//   // inverting y axis by setting chartHeight to the x coordinate
//   .range([chartHeight, 0])

// const xScale0 = d3.scaleBand()
//   .domain(sumPerMonth.map(d => (d.act_start_date)))
//   .range([0, chartWidth])
//   .padding(0.05)

//   const xScale1 = d3.scaleBand()
//     .domain(['fin_est_labor_expense', 'fin_act_labor_expense'])
//     .range([0, xScale0.bandwidth()])
//     // .padding(0.05)

// // Generating axis from scales
// const xAxis = d3.axisBottom(xScale0)
// const yAxis = d3.axisLeft(yScale)

// chartG.append("g")
// .call(yAxis)

// chartG.append("g")
// .attr("transform", `translate(0, ${chartHeight})`)
// .call(xAxis)

// // Adding Est Labor Exp Bars
// chartG.selectAll(".bar.fin_est_labor_expense")
//   .data(sumPerMonth)
//   .enter()
//   .append("rect")
//   .attr("class", "bar-est_labor-exp")
// .style("fill","blue")  
//   .attr("x", d => xScale1("act_start_date"))
//   .attr("y", d => yScale(d.fin_est_labor_expense))
//   .attr("width", xScale1.bandwidth())
//   .attr("height", d => chartHeight - yScale(d.fin_est_labor_expense))

//   // Adding Act Labor Exp Bars
// chartG.selectAll(".bar.fin_act_labor_expense")
// .data(sumPerMonth)
// .enter()
// .append("rect")
// .attr("class", "bar-fin_act_labor_expense")
// .style("fill","red")
// .attr("x", d => xScale1('act_start_date'))
// .attr("y", d => yScale(d.fin_act_labor_expense))
// .attr("width", xScale1.bandwidth())
// .attr("height", d => chartHeight - yScale(d.fin_est_labor_expense))
  
  // .attr("x", d => x(d.month))
  // .attr("y", d => y(d.fin_est_labor_expense))
  // .attr("height", d => chartHeight - y(d.fin_est_labor_expense))
  // .attr("width", x.bandwidth())


//   const container = d3.select('#time_series'),
//     width = 520,
//     height = 220,
//     margin = {top: 30, right: 20, bottom: 30, left: 50},
//     barPadding = .2,
//     axisTicks = {qty: 5, outerSize: 0, dateFormat: '%m-%d'};
  
//   const svg = container
//     .append("svg")
//     .attr("width", width)
//     .attr("height", height)
//     .append("g")
//     .attr("transform", `translate(${margin.left},${margin.top})`);

//     const xScale0 = d3.scaleBand()
//       .range([0, width - margin.left - margin.right])
//       .padding(barPadding)
//     const xScale1 = d3.scaleBand()
//     const yScale = d3.scaleLinear()
//       .range([height - margin.top - margin.bottom, 0]);

//   const xAxis = d3.axisBottom(xScale0).
//     tickSizeOuter(axisTicks.outerSize);
//   const yAxis = d3.axisLeft(yScale)
//     .ticks(axisTicks.qty)
//     .tickSizeOuter(axisTicks.outerSize);  

//     xScale0.domain(sumPerMonth.map(d => d.act_start_date))

//     xScale1.domain(['fin_est_labor_expense', 'fin_act_labor_expense'])
//       .range([0, xScale0.bandwidth()])

//      yScale.domain([0, d3.max(sumPerMonth, d => d.fin_est_labor_expense > d.fin_act_labor_expense ? d.fin_est_labor_expense : d.fin_act_labor_expense)])

//   var model_name = svg.selectAll(".act_start_date")
//     .data(sumPerMonth)
//     .enter()
//     .append("g")
//     .attr("class", "act_start_date")
//     .attr("transform", d => `translate(${xScale0(d.model_name)},0)`);

//     /* Add field1 bars */
// model_name.selectAll(".bar.fin_est_labor_expense")
// .data(d => [d])
// .enter()
// .append("rect")
// .attr("class", "bar-fin_est_labor_expense")
// .style("fill","blue")
// .attr("x", d => xScale1('fin_est_labor_expense'))
// .attr("y", d => yScale(d.fin_est_labor_expense))
// .attr("width", xScale1.bandwidth())
// .attr("height", d => {
//   return height - margin.top - margin.bottom - yScale(d.fin_est_labor_expense)
// });

// /* Add field2 bars */
// model_name.selectAll(".bar.fin_act_labor_expense")
// .data(d => [d])
// .enter()
// .append("rect")
// .attr("class", "bar-fin_act_labor_expense")
// .style("fill","red")
// .attr("x", d => xScale1('fin_act_labor_expense'))
// .attr("y", d => yScale(d.fin_act_labor_expense))
// .attr("width", xScale1.bandwidth())
// .attr("height", d => {
//   return height - margin.top - margin.bottom - yScale(d.fin_act_labor_expense)
// });

// // Add the X Axis
// svg.append("g")
//      .attr("class", "x axis")
//      .attr("transform", `translate(0,${height - margin.top  - margin.bottom})`)
//      .call(xAxis);// Add the Y Axis
// svg.append("g")
//      .attr("class", "y axis")
//      .call(yAxis);




// load the data
projectArray = Object.keys(project_list).map((i) => project_list[i]);
// console.log(projectArray)

// // Sorting data by month
// const sortedData = projectArray.slice().sort((a,b) => new Date(b.act_start_date) - new Date(a.act_start_date))
// console.log(sortedData)

// parsing through data to pull data needed for bar chart
const chartData = projectArray.map(({act_start_date, fin_est_labor_expense, fin_act_labor_expense}) => ({act_start_date, fin_est_labor_expense: parseFloat(fin_est_labor_expense), fin_act_labor_expense: parseFloat(fin_act_labor_expense)}));
// console.log(chartData)

// Grouping dates into months
const mapDayToMonth = chartData.map(x => ({...x, act_start_date: new Date(x.act_start_date).getMonth()}));

// // summing revenue per month by using reduce function
const sumPerMonth = mapDayToMonth.reduce(function(allDates, date) {
  if (allDates.some(function(e) {
      return e.act_start_date === date.act_start_date
    })) {
    allDates.filter(function(e) {
      return e.act_start_date === date.act_start_date
    })[0].fin_est_labor_expense += +date.fin_est_labor_expense
  } else {
    allDates.push({
      act_start_date: date.act_start_date,
      fin_est_labor_expense: +date.fin_est_labor_expense,
      fin_act_labor_expense: +date.fin_act_labor_expense,
    })
  }
  return allDates
}, []);
console.log(sumPerMonth)

// Sorting data by month
const data = sumPerMonth.slice().sort((a,b) => new Date(a.act_start_date) - new Date(b.act_start_date))
console.log(data)

// const month = ["Jan", "Feb","Mar", "Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
// const data = dataSorted.map(o => ({
//   ...o,
//   act_start_date: month[o.act_start_date - 2],
// }))
// console.log(data)





const margin = {top: 70, right: 20, bottom: 70, left: 100},
    width = 1135 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// Parse the date / time
// var	parseDate = d3.isoParse

const x = d3.scaleBand()
.rangeRound([0, width], .05)
.padding(0.1);

const y = d3.scaleLinear().range([height, 0]);

const xAxis = d3.axisBottom()
    .scale(x)
    // .tickFormat(d3.timeFormat("%b"));

const yAxis = d3.axisLeft()
    .scale(y)
    .ticks(10);

const svg = d3.select("#estimate-to-actual").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

data.forEach(d => {
  d.act_start_date = parseInt(d.act_start_date);
  d.fin_act_labor_expense = +d.fin_act_labor_expense;
});

  x.domain(data.map(d => d.act_start_date));
  y.domain([0, d3.max(data, d => d.fin_est_labor_expense)]); 

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis.ticks(null).tickSize(0))
      .selectAll("text")
      .style("text-anchor", "middle")


  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis.ticks(null).tickSize(-width))
    .append("text")
      .attr("y", 6)
      .style("text-anchor", "middle")
      .text("Value");

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
  
  svg.selectAll("lines")
      .data(data)
    .enter().append("line")
      .style("fill", 'none')
  		.attr("x1", d => x(d.act_start_date) + x.bandwidth() +5)
      .attr("x2", d => x(d.act_start_date) -5)
   .attr("y1", d => y(+d.fin_est_labor_expense))
      .attr("y2", d => y(+d.fin_est_labor_expense))
  		.style("stroke-dasharray", [3,3])
  		.style("stroke", "#eb2828")
  .style("stroke-width", 2)
  
svg.append ('text')
    .attr("class", 'xAxisLabel')
    .attr("y", 525)
    .attr("x", width/2)
    .attr("fill", "#635f5d")
    .style('font-size', '2.5em')
    .text( "Months")

  svg.append ('text')
      .attr("class", "Title")
      .attr("y", -10)
      .attr("x", 160)
      .attr("fill", "#635f5d")
      .style("font-size", "3.5em")
      .text("Estimate vs. Actual Labor Expense")

    svg.append('text')
      .attr('class', 'Axis-Label')
      .attr('y', -55)
      .attr('x', -380)
      .attr('fill', 'black')
      .attr('transform', `rotate(-90)`)
      .attr("fill", "#635f5d")
      .style('font-size', '2.5em')
      .text("Labor Expense ($)");






