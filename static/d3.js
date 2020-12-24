// const { range } = require("d3");

// const { scaleBand } = require("d3");

// load the data
projectArray = Object.keys(project_list).map((i) => project_list[i]);
console.log(projectArray);

// parsing through data to pull data needed for bar chart
const data = projectArray.map(({act_start_date, fin_est_labor_expense, fin_act_labor_expense}) => ({act_start_date, fin_est_labor_expense: parseFloat(fin_est_labor_expense), fin_act_labor_expense: parseFloat(fin_act_labor_expense)}));
console.log(data)
// grouping all start dates by month
const mapDayToMonth = data.map(x => ({...x, act_start_date: new Date(x.act_start_date).getMonth()}));
console.log(mapDayToMonth)

// summing revenue per month by using reduce function
const sumPerMonthEst = mapDayToMonth.reduce(function(allDates, date) {
  if (allDates.some(function(e) {
      return e.act_start_date === date.act_start_date
    })) {
    allDates.filter(function(e) {
      return e.act_start_date === date.act_start_date
    })[0].fin_est_labor_expense += +date.fin_est_labor_expense
  } else {
    allDates.push({
      act_start_date: date.act_start_date,
      fin_est_labor_expense: +date.fin_est_labor_expense
    })
  }
  return allDates
}, []);

console.log(sumPerMonthEst)
// sorting sumPerMonthEst object
sumPerMonthEst.sort(function(l,r){
  return l.act_start_date - r.act_start_date;
});


const svgHeight = 600
const svgWidth = 1135

const margin = {
  top: 50,
  right: 50,
  bottom: 50,
  left: 50
}

// set chart demensions
chartHeight = svgHeight - margin.top - margin.bottom
chartWidth = svgWidth - margin.left - margin.right

// defining svg and placing it
const svg = d3.select("#time_series").append("svg")
  .attr("height", svgHeight)
  .attr("width", svgWidth)

// setting up chart group
const chartG = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`)

// setting scales
const y = d3.scaleLinear()
  .domain([0, d3.max(sumPerMonthEst.map(d => d.fin_est_labor_expense))])
  // inverting y axis by setting chartHeight to the x coordinate
  .range([chartHeight, 0])

const x = d3.scaleBand()
  .domain(sumPerMonthEst.map(d => (d.act_start_date)))
  .range([0, chartWidth])
  .padding(0.05)

// Generating axis from scales
const xAxis = d3.axisBottom(x)
const yAxis = d3.axisLeft(y)

chartG.append("g")
.call(yAxis)

chartG.append("g")
.attr("transform", `translate(0, ${chartHeight})`)
.call(xAxis)

chartG.selectAll("rect")
.data(sumPerMonthEst)
.enter()
.append("rect")
.attr("x", d => x(d.act_start_date))
.attr("y", d => y(d.fin_est_labor_expense))
.attr("height", d => chartHeight - y(d.fin_est_labor_expense))
.attr("width", x.bandwidth())


// // set the ranges
// var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.05);
// var y = d3.scale.linear().range([height, 0]);

// // define the axis
// var xAxis = d3.svg.axis().scale(x).orient("bottom");

// var yAxis = d3.svg.axis().scale(y).orient("left").ticks(10);

// // add the SVG element
// var svg = d3
//   .select("#time_series")
//   .append("svg")
//   .attr("width", width + margin.left + margin.right)
//   .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//   .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


// d3.json("../static/result.json", function (error, data) {
//   data.forEach(function (d) {
//     d.Name = d.name;
//     d.Rev = +d.revenue;
//   });

  // scale the range of the data
//   x.domain(
//     data.map(function (d) {
//       return d.Name;
//     })
//   );
//   y.domain([
//     0,
//     d3.max(data, function (d) {
//       return d.Rev;
//     }),
//   ]);

//   // add axis
//   svg
//     .append("g")
//     .attr("class", "x axis")
//     .attr("transform", "translate(0," + height + ")")
//     .call(xAxis)
//     .selectAll("text")
//     .attr("dy", "1.55em")
//     .call(wrap, x.rangeBand());
//   // .attr("transform", "rotate(-90)" );

//   svg
//     .append("g")
//     .attr("class", "y axis")
//     .call(yAxis)
//     .append("text")
//     .attr("transform", "rotate(-90)")
//     .attr("y", 5)
//     .attr("dy", ".71em")
//     .style("text-anchor", "end")
//     .text("Revenue");

//   // Add bar chart
//   svg
//     .selectAll("bar")
//     .data(data)
//     .enter()
//     .append("rect")
//     .attr("class", "bar")
//     .attr("x", function (d) {
//       return x(d.Name);
//     })
//     .attr("width", x.rangeBand())
//     .attr("y", function (d) {
//       return y(d.Rev);
//     })
//     .attr("height", function (d) {
//       return height - y(d.Rev);
//     })
//     .attr("fill", function (d) {
//       return "#337ab7";
//     });

//   var sum = d3.sum(data, function (d) {
//     return d.Rev;
//   });
//   var average = sum / data.length;

//   var line = d3.svg
//     .line()
//     .x(function (d, i) {
//       return x2(d.Rev) + i;
//     })
//     .y(function (d, i) {
//       return y(average);
//     });

//   svg.append("path").datum(data).attr("class", "mean").attr("d", line);

//   svg
//     .append("text")
//     .attr("transform", "translate(" + (width + 3) + "," + y(average) + ")")
//     .attr("dy", "1em")
//     .attr("text-anchor", "end")
//     .style("fill", "red")
//     .html("Average = $" + average);
//   s;
// });

// function wrap(text, width) {
//   text.each(function () {
//     var text = d3.select(this),
//       words = text.text().split(/\s+/).reverse(),
//       word,
//       line = [],
//       lineNumber = 0,
//       lineHeight = 1.1, // ems
//       y = text.attr("y"),
//       dy = parseFloat(text.attr("dy")),
//       tspan = text
//         .text(null)
//         .append("tspan")
//         .attr("x", 0)
//         .attr("y", y)
//         .attr("dy", dy + "em");
//     while ((word = words.pop())) {
//       line.push(word);
//       tspan.text(line.join(" "));
//       if (tspan.node().getComputedTextLength() > width) {
//         line.pop();
//         tspan.text(line.join(" "));
//         line = [word];
//         tspan = text
//           .append("tspan")
//           .attr("x", 0)
//           .attr("y", y)
//           .attr("dy", ++lineNumber * lineHeight + dy + "em")
//           .text(word);
//       }
//     }
//   });
// }
