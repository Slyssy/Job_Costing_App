// set the dimensions of the canvas
var margin = { top: 20, right: 20, bottom: 70, left: 140 },
  width = 600 - margin.left - margin.right,
  height = 300 - margin.top - margin.bottom;

// set the ranges
var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.05);
var y = d3.scale.linear().range([height, 0]);

// define the axis
var xAxis = d3.svg.axis().scale(x).orient("bottom");

var yAxis = d3.svg.axis().scale(y).orient("left").ticks(10);

// add the SVG element
var svg = d3
  .select("#bar")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// load the data
d3.json("../static/result.json", function (error, data) {
  data.forEach(function (d) {
    d.Name = d.name;
    d.Rev = +d.revenue;
  });

  // scale the range of the data
  x.domain(
    data.map(function (d) {
      return d.Name;
    })
  );
  y.domain([
    0,
    d3.max(data, function (d) {
      return d.Rev;
    }),
  ]);

  // add axis
  svg
    .append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .selectAll("text")
    .attr("dy", "1.55em")
    .call(wrap, x.rangeBand());
  // .attr("transform", "rotate(-90)" );

  svg
    .append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 5)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Revenue");

  // Add bar chart
  svg
    .selectAll("bar")
    .data(data)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("x", function (d) {
      return x(d.Name);
    })
    .attr("width", x.rangeBand())
    .attr("y", function (d) {
      return y(d.Rev);
    })
    .attr("height", function (d) {
      return height - y(d.Rev);
    })
    .attr("fill", function (d) {
      return "#337ab7";
    });

  var sum = d3.sum(data, function (d) {
    return d.Rev;
  });
  var average = sum / data.length;

  var line = d3.svg
    .line()
    .x(function (d, i) {
      return x2(d.Rev) + i;
    })
    .y(function (d, i) {
      return y(average);
    });

  svg.append("path").datum(data).attr("class", "mean").attr("d", line);

  svg
    .append("text")
    .attr("transform", "translate(" + (width + 3) + "," + y(average) + ")")
    .attr("dy", "1em")
    .attr("text-anchor", "end")
    .style("fill", "red")
    .html("Average = $" + average);
  s;
});

function wrap(text, width) {
  text.each(function () {
    var text = d3.select(this),
      words = text.text().split(/\s+/).reverse(),
      word,
      line = [],
      lineNumber = 0,
      lineHeight = 1.1, // ems
      y = text.attr("y"),
      dy = parseFloat(text.attr("dy")),
      tspan = text
        .text(null)
        .append("tspan")
        .attr("x", 0)
        .attr("y", y)
        .attr("dy", dy + "em");
    while ((word = words.pop())) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text
          .append("tspan")
          .attr("x", 0)
          .attr("y", y)
          .attr("dy", ++lineNumber * lineHeight + dy + "em")
          .text(word);
      }
    }
  });
}
