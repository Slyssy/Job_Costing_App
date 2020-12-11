// Time Series Chart that tracks Revenue for Each Month

function makeplot() {
  {
  }
  Plotly.d3.json("..//static/result.json", function (err, rows) {
    function unpack(rows, key) {
      return rows.map(function (row) {
        return row[key];
      });
    }
    var trace1 = {
      type: "bar",
      mode: "lines",
      name: "revenue",
      x: unpack(rows, "act_start_date", "act_end_date"),
      y: unpack(rows, "fin_act_revenue"),
      line: { color: "#17BECF" },
    };
    var trace2 = {
      type: "bar",
      mode: "lines",
      name: "est_labor_expense",
      x: unpack(rows, "act_start_date", "act_end_date"),
      y: unpack(rows, "fin_est_revenue"),
      line: { color: "#7F7F7F" },
    };
    var data = [trace1, trace2];
    var layout = {
      title: "",
      xaxis: {
        autorange: true,
        range: ["act_start_date", "act_comp_date"],
        rangeselector: {
          buttons: [
            {
              count: 1,
              label: "1m",
              step: "month",
              stepmode: "backward",
            },
            {
              count: 6,
              label: "6m",
              step: "month",
              stepmode: "backward",
            },
            { step: "all" },
          ],
        },
        rangeslider: { range: ["act_start_date", "act_end_date"] },
        type: "date",
      },
      yaxis: {
        autorange: true,
        range: [min("revenue"), max("revenue")],
        type: "linear",
      },
    };
    Plotly.newPlot("time_series", data, layout);
  });
}
